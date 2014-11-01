#!/usr/bin/python3

import unittest
import insummer 
from insummer.kbtool import get_entity_link

class mytest(unittest.TestCase):
    def setUp(self):
        pass
        
    def testEntityLink(self):
        sentence = 'How to handle a 1.5 year old when hitting?'
        result = get_entity_link(sentence)

        print result

    

if __name__ == '__main__':
    unittest.main()
