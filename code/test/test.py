#!/usr/bin/python3

import sys
sys.path.append("..")
import insummer
import unittest
from insummer.util import NLP



class mytest(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_norm_text(self):
        nlp = NLP()
        self.assertEqual(nlp.norm_text('dogs'),'dog','测试归一化句子')
    
if __name__ == '__main__':
    unittest.main()
