#coding: utf-8
#!/usr/bin/python

import pycurl
from StringIO import StringIO
from urllib import urlencode

from read_conf import config

slconf = config("/home/lavi/project/graduate_project/conf/kbtool.conf")

#得到实体链接信息，即该句子的所有实体
def get_entity_link(sentence):
    post_data = {'text':sentence,'confidence':slconf['spotlight_confidence'],'support':slconf['spotlight_support']}

    postfields = urlencode(post_data)

    buffer = StringIO()
    curl1 = pycurl.Curl()
    curl1.setopt(curl1.URL, 'http://spotlight.dbpedia.org/rest/annotate')
    curl1.setopt(curl1.POSTFIELDS,postfields)
    curl1.setopt(curl1.WRITEDATA, buffer)
    curl1.perform()
    curl1.close()

    body = buffer.getvalue()

    return body


if __name__ == '__main__':
    sentence = ''

    get_entity_link(sentence)

    
