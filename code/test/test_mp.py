#!/usr/bin/python3
import time
clock = time.time


import threading
import queue as Queue

class NoResultsPending(Exception):
    """All work requests have been processed."""
    pass
class NoWorkersAvailable(Exception):
    """No worker threads available to process remaining requests."""
    pass

class WorkerThread(threading.Thread):
    """Background thread connected to the requests/results queues.

    A worker thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.
    """

    def __init__(self, requestsQueue, resultsQueue, **kwds):
        """Set up thread in damonic mode and start it immediatedly.

        requestsQueue and resultQueue are instances of Queue.Queue passed
        by the ThreadPool class when it creates a new worker thread.
        """
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self.workRequestQueue = requestsQueue
        self.resultQueue = resultsQueue
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """Repeatedly process the job queue until told to exit.
        """

        while not self._dismissed.isSet():
            # thread blocks here, if queue empty
            request = self.workRequestQueue.get()
            if self._dismissed.isSet():
                # return the work request we just picked up
                self.workRequestQueue.put(request)
                break # and exit
            # XXX catch exceptions here and stick them to request object
            self.resultQueue.put(
                (request, request.callable(*request.args, **request.kwds))
            )

    def dismiss(self):
        """Sets a flag to tell the thread to exit when done with current job.
        """

        self._dismissed.set()


class WorkRequest:
    """A request to execute a callable for putting in the request queue later.

    See the module function makeRequests() for the common case
    where you want to build several work requests for the same callable
    but different arguments for each call.
    """

    def __init__(self, callable, args=None, kwds=None, requestID=None,
      callback=None):
        """A work request consists of the a callable to be executed by a
        worker thread, a list of positional arguments, a dictionary
        of keyword arguments.

        A callback function can be specified, that is called when the results
        of the request are picked up from the result queue. It must accept
        two arguments, the request object and it's results in that order.
        If you want to pass additional information to the callback, just stick
        it on the request object.

        requestID, if given, must be hashable as it is used by the ThreadPool
        class to store the results of that work request in a dictionary.
        It defaults to the return value of id(self).
        """
        if requestID is None:
            self.requestID = id(self)
        else:
            self.requestID = requestID
        self.callback = callback
        self.callable = callable
        self.args = args or []
        self.kwds = kwds or {}


class ThreadPool:
    """A thread pool, distributing work requests and collecting results.

    See the module doctring for more information.
    """

    def __init__(self, num_workers, q_size=0):
        """Set up the thread pool and start num_workers worker threads.

        num_workers is the number of worker threads to start initialy.
        If q_size > 0 the size of the work request is limited and the
        thread pool blocks when queue is full and it tries to put more
        work requests in it.
        """

        self.requestsQueue = Queue.Queue(q_size)
        self.resultsQueue = Queue.Queue()
        self.workers = []
        self.workRequests = {}
        self.createWorkers(num_workers)

    def createWorkers(self, num_workers):
        """Add num_workers worker threads to the pool."""

        for i in range(num_workers):
            self.workers.append(WorkerThread(self.requestsQueue,
              self.resultsQueue))

    def dismissWorkers(self, num_workers):
        """Tell num_workers worker threads to to quit when they're done."""

        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()

    def putRequest(self, request):
        """Put work request into work queue and save for later."""

        self.requestsQueue.put(request)
        self.workRequests[request.requestID] = request

    def poll(self, block=False):
        """Process any new results in the queue."""
        while 1:
            try:
                # still results pending?
                if not self.workRequests:
                    raise NoResultsPending
                # are there still workers to process remaining requests?
                elif block and not self.workers:
                    raise NoWorkersAvailable
                # get back next results
                request, result = self.resultsQueue.get(block=block)
                # and hand them to the callback, if any
                if request.callback:
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Queue.Empty:
                break

    def wait(self):
        """Wait for results, blocking until all have arrived."""

        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break

def makeRequests(callable, args_list, callback=None):
    """Convenience function for building several work requests for the same
    callable with different arguments for each call.

    args_list contains the parameters for each invocation of callable.
    Each item in 'argslist' should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    callback is called when the results arrive in the result queue.
    """

    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
              WorkRequest(callable, item[0], item[1], callback=callback))
        else:
            requests.append(
              WorkRequest(callable, [item], None, callback=callback))
    return requests


################
# USAGE EXAMPLE
################

import sys
sys.path.append("..")
import insummer
from insummer.knowledge_base import MultiInsunnetFinder as MFinder
from insummer.knowledge_base import InsunnetFinder as Finder
from insummer.knowledge_base.entity_lookup import ConceptnetEntityLookup,InsunnetEntityLookup

finder = Finder()
mfinder = MFinder()
Searcher = InsunnetEntityLookup

import multiprocessing as mp

base = {'male', 'battery', 'barrier', 'automobile', 'admittance', 'admission', 'way', 'dobbin', 'entrée', 'access', 'nag', 'car', 'jade', 'ink', 'bung', 'vehicle', 'carload', 'railcar', 'auto_insurance', 'carriage', 'motor', 'gondola', 'electricity', 'car_battery', 'wagonload', 'entry', 'motorcar', 'auto', 'male-to-female', 'electroconvulsive_therapy', 'wagon', 'tramcar', 'plug', 'ect', 'military_battery', 'stopper', 'electric_power', 'electrical_power', 'username', 'accumulator', 'basket', 'hack'}


entity = 'bike'

def find_weight(target):
    result = []
    for ent in base:
        weight = finder.lookup_weight(ent,entity)
        if weight != 0 :
            result.append((ent,1))
        else:
            result.append((ent,0))

    return result

    
def fw(ent):
    mfinder = MFinder()
    print("base %s"%(ent))
    expand = {}
    
    #先找到所有的关联实体
    searcher = Searcher()
    cand = searcher.relate_entity(ent)

    length = len(cand)

    indx = 0
    for acand in cand:
        if indx % 10 == 0:
            print("基实体 %s 进行到%s"%(ent,indx/length))
        if acand in expand:
            pass
        else:
            total = 0
            for bentity in base:
                w = mfinder.lookup_weight(bentity,acand)
                total += w

            expand[acand] = total
        indx += 1
    return expand

def adres(request,ent):
    res.append(ent)
    
def mfind_weight():
    pool = mp.Pool(processes=16)
    results = [pool.apply_async(fw, args=(ent,)) for ent in base]
    output = [p.get() for p in results]
    print(output)

    

if __name__ == '__main__':
    '''
    total = 0
    n = 10
    for i in range(n):
        begin = clock()
        result = find_weight()
        end = clock()
        total += (end-begin)

    print(total/n)
    total = 0
    '''

    #begin = clock()
    #result = mfind_weight()
    #end = clock()

    cand = range(31)
    print(spli(cand,5))
