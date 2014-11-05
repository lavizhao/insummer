#!/usr/bin/python3

import sys
sys.path.append("..")
import insummer
import unittest
from insummer.util import NLP
from insummer.conceptnet_tool import conceptnet_has_concept as chc



class mytest(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_norm_text(self):
        nlp = NLP()
        self.assertEqual(nlp.norm_text('dogs'),'dog','测试归一化句子')

    def test_has_concept(self):
        self.assertEqual(chc('dog'),True,'测试在不在知识库中')
        self.assertEqual(chc('dogs'),True,'测试在不在知识库中')
        self.assertEqual(chc('cats'),True,'测试在不在知识库中')
        self.assertEqual(chc('names'),True,'测试在不在知识库中')
    
if __name__ == '__main__':
    unittest.main()
