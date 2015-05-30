#!/usr/bin/python3

import json

from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import abort, redirect, url_for

from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required


from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT,STORED
import whoosh.index as index

import sys
sys.path.append("..")
import insummer

from insummer.summarization.ilp import dis_ilp as DI
from insummer.common_type import Question,Answer,build_question
from insummer.util import NLP

nlp = NLP()

app = Flask(__name__)



Bootstrap(app)
# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
'6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'


class search_form(Form):
    name = StringField('', validators=[DataRequired()])

index_dir = "/home/lavi/project/insummer/index"
ix = index.open_dir(index_dir)
searcher = ix.searcher()



def get_question_title(words):
    qp = QueryParser("title", ix.schema)
    words = words.replace("_"," ")
    q = qp.parse(words)
    results = searcher.search(q)

    res = ""
    print("here")
    for indx,a in enumerate(results):
        title = a["title"]
        qid = a["qid"]
        res += u'''<p><a href="http://127.0.0.1:5000/qid/%s">问题%s  %s</a></p>\n 
        <hr/>\n
        '''%(qid,indx+1,title)

    return res,words


@app.route('/', methods=('GET','POST'))
def main():
    print("main")
    form = search_form()
    if form.validate_on_submit():
        words = form.name.data
        sp = words.split()
        words = '_'.join(sp)
        murl = url_for('qsearch',words=words)
        return redirect(murl)
        
    return render_template('main.html',form=form)

@app.route('/search/<words>')
def qsearch(words):
    print("search")
    form2 = search_form()
    questions,title = get_question_title(words)
        
    return render_template('qsearch.html',qtitle=title,result = questions,form=form2)

    
@app.route('/qid/<qid>')    
def dis_question(qid):
    qp = QueryParser("qid", ix.schema)
    q = qp.parse(qid)
    results = searcher.search(q)
    res = results[0]

    form3 = search_form()

    nbest = json.loads(res["nbest"])

    ans_content = ""
    for indx,a in enumerate(nbest):
        ans_content += u'''<p>答案%s 单词数%s</p>
        <p>%s</p>\n 
        <hr/>\n
        '''%(indx,nlp.sentence_length(a),a)

    tquestion = build_question(title=res["title"],content=res["content"],best=res["best"],nbest=nbest)
    di = DI(tquestion,100)

    summarization = di.extract()

    summarization = ''.join(summarization)
    
    return render_template('qdis.html',qtitle=res["title"],best=res["best"],form=form3,result=ans_content,content=res["content"],summarization=summarization)

if __name__ == '__main__':
    app.run(debug=True)
