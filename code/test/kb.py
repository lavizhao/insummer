#!/usr/bin/python3

'''
测试knowledge_base
'''

import sys
sys.path.append("..")
import insummer

from insummer.knowledge_base import concept_tool,InsunnetFinder
from insummer.knowledge_base.relation import relation_tool
from insummer.knowledge_base.entity_lookup import ConceptnetEntityLookup,InsunnetEntityLookup

import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.cn = concept_tool()
        self.re = relation_tool()
        self.finder = InsunnetFinder()
        self.cel = ConceptnetEntityLookup()
        self.iel = InsunnetEntityLookup()
        
    #测试InsunnetFinder
    def testFinderLookup(self):
        #随便输一个单词返回结果应不为0
        cp1 = '/c/en/apple'
        self.assertEqual(len(self.finder.lookup(cp1))!=0,True)

        cp2 = 'apple'
        self.assertEqual(len(self.finder.lookup(cp2))!=0,True)

        cp3 = 'lajsljflkj'
        self.assertEqual(len(self.finder.lookup(cp3))==0,True)

        cp4 = 'band'
        result = self.finder.lookup(cp4)[:1000]
        print("band 的搜索结果",len(result))
        for i in result:
            print(i)


    def testFinderWeight(self):
        cp1 = '/c/en/apple'
        cp2 = 'pie'
        self.assertEqual(self.finder.lookup_weight(cp1,cp2)!=0,True)

    #测试concept tool
    def testIsEnglishConcept(self):
        #test single    
        cp1 = '/c/en/fuck'
        self.assertEqual(self.cn.is_english_concept(cp1),True)
        
        cp2 = '/c/de/fuck'
        self.assertEqual(self.cn.is_english_concept(cp2),False)

        cp3 = 'fuck'
        self.assertEqual(self.cn.is_english_concept(cp3),True)

        #test both
        self.assertEqual(self.cn.both_english_concept(cp1,cp2),False)
        self.assertEqual(self.cn.both_english_concept(cp1,cp3),True)
        self.assertEqual(self.cn.both_english_concept(cp2,cp3),False)

    def testConceptName(self):
        cp1 = '/c/en/fuck'
        self.assertEqual(self.cn.concept_name(cp1),'fuck')

        cp2 = 'fuck'
        self.assertEqual(self.cn.concept_name(cp2),'fuck')

        cp3 = '/c/de/fuck'
        self.assertEqual(self.cn.concept_name(cp3),'wojiaozhaoximo')

        cp4 = 0
        self.assertEqual(self.cn.concept_name(cp4),'0')


    def testEntityEqual(self):
        cp1 = '/c/en/fuck'
        cp2 = 'fuck'
        cp3 = 'shabi'
        self.assertEqual(self.cn.entity_equal(cp1,cp2),True)
        self.assertEqual(self.cn.entity_equal(cp1,cp3),False)
        self.assertEqual(self.cn.entity_equal(cp2,cp3),False)

    def testAddPrefix(self):
        cp1 = '/c/en/fuck'
        cp2 = 'fuck'
        cp3 = '/c/de/fuck'
        self.assertEqual(self.cn.add_prefix(cp1),'/c/en/fuck')
        self.assertEqual(self.cn.add_prefix(cp2),'/c/en/fuck')
        self.assertEqual(self.cn.add_prefix(cp3),'/c/en/wojiaozhaoximo')

    def testConceptHasConcept(self):
        cp1 = 'fuck'
        self.assertEqual(self.cn.conceptnet_has_concept(cp1),True)
        self.assertEqual(self.cn.kb_has_concept(cp1),True)

        cp2 = '/c/en/fuck'
        self.assertEqual(self.cn.kb_has_concept(cp2),True)

        cp3 = '/c/de/fuck'
        self.assertEqual(self.cn.kb_has_concept(cp3),False)

    
    #测试relation tool
    def testIsRelation(self):
        rel1 = '/r/RelatedTo'
        self.assertEqual(self.re.is_relation(rel1),True)

        rel2 = 'RelatedTo'
        self.assertEqual(self.re.is_relation(rel2),True)

        rel3 = 'relate'
        self.assertEqual(self.re.is_relation(rel3),False)

        rel4 = 'other'
        self.assertEqual(self.re.is_relation(rel4),False)

    def testIsPos(self):
        rel1 = '/r/RelatedTo'
        self.assertEqual(self.re.is_pos(rel1),True)

        rel2 = 'RelatedTo'
        self.assertEqual(self.re.is_pos(rel2),True)

        rel3 = '/r/NotRelatedTo'
        self.assertEqual(self.re.is_pos(rel3),False)

        rel4 = '/r/IsA'
        self.assertEqual(self.re.is_pos(rel4),True)

    def testRelName(self):
        rel1 = '/r/RelatedTo'
        self.assertEqual(self.re.rel_name(rel1),'RelatedTo')

        rel2 = 'RelatedTo'
        self.assertEqual(self.re.rel_name(rel2),'RelatedTo')

        rel3 = '/r/NotRelatedTo'
        self.assertEqual(self.re.rel_name(rel3),'RelatedTo')

        rel4 = '/r/IsA'
        self.assertEqual(self.re.rel_name(rel4),'IsA')

        rel5 = '/r/fuck'
        self.assertEqual(self.re.rel_name(rel5),'fuck')

        rel6 = 'fuck'
        self.assertEqual(self.re.rel_name(rel6),'fuck')

    def testGetRelIndx(self):
        rel1 = '/r/RelatedTo'
        self.assertEqual(self.re.get_rel_indx(rel1),0)

        rel2 = '/r/MemberOf'
        self.assertEqual(self.re.get_rel_indx(rel2),22)

        rel3 = 'RelatedTo'
        self.assertEqual(self.re.get_rel_indx(rel3),0)

        rel4 = 'sdfsf'
        self.assertEqual(self.re.get_rel_indx(rel4),30)

    def testsynonym_type(self):
        rel1 = '/r/RelatedTo'    
        self.assertEqual(self.re.synonym_type(rel1),False)

        rel2 = '/r/Synonym'    
        self.assertEqual(self.re.synonym_type(rel2),True)

        rel3 = 'RelatedTo'    
        self.assertEqual(self.re.synonym_type(rel3),False)

        rel4 = 'Synonym'    
        self.assertEqual(self.re.synonym_type(rel4),True)

        rel5 = 'fuck'
        self.assertEqual(self.re.synonym_type(rel5),False)


    #测试 InsunnetEntityLookup
    def testInsRel(self):
        cp1 = 'apple'
        self.assertEqual(len(self.iel.synonym_entity(cp1))!=0,True)
        self.assertEqual(len(self.iel.relate_entity(cp1))!=0,True)

        cp2 = 'tree'
        self.assertEqual(len(self.iel.synonym_entity(cp2))!=0,True)
        self.assertEqual(len(self.iel.relate_entity(cp2))!=0,True)

    

    
        
if __name__ == '__main__':
    unittest.main()


