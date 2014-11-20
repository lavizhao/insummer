#!/usr/bin/python3

import sys
sys.path.append("..")
import insummer
from insummer.query_expansion.entity_finder import example_entity_finder,NgramEntityFinder
from insummer.read_conf import config
from insummer.common_type import Question
from insummer.util import NLP

nlp = NLP()

title = "How do Motorcycles pollute?"

answer = " Motorcycles and scooters are an appealing alternative to shelling out big bucks filling up the family truckster, which is one reason sales are going through the roof. But riding on two wheels may not be any more environmentally responsible than riding on four. \
Turns out the average motorcycle is 10 times more polluting per mile than a passenger car, light truck or SUV. It seems counter-intuitive, because motorcycles are about twice as fuel-efficient as cars and emit a lot less C02. \
So what gives? \
Susan Carpenter lays it all out in a Los Angeles Times column. She found that, although motorcycles and scooters comprise 3.6 percent of registered vehicles in California and 1 percent of vehicle miles traveled, they account for 10 percent of passenger vehicles' smog-forming emissions. \
Motorcycle engines are twice as efficient as automobile engines, she notes, so they generally emit less carbon dioxide. But they emit large amounts of nitrogen oxides, which along with hydrocarbons and carbon monoxide are measured by state and federal air quality regulators to determine whether vehicles meet emissions rules. \
Catalytic converters and other emissions control devices would clean things up, but they're often too big, too heavy or too hot to install on motorcycles. For that reason and others that Carpenter outlines in the column, the Environmental Protection Agency and California Air Resources Board are more lenient when it comes to motorcycle emissions. \
\"The emissions picture [for motorcycles] is pretty grim,\" she quotes John Swanton of the Air Resources Board saying, but we think it's fair for where motorcycles are today. "

def test1():
    naive_question = Question("sh","","","")

    my = example_entity_finder(naive_question)

    #my.find()
    #my.print()
    
if __name__ == '__main__':
    #test1()

    result = nlp.sent_tokenize(answer)
    for sent in result:
        ngram = NgramEntityFinder(sent)

        #ngram.find(display=True)
        ngram.extract_entity(display=True)
    

