# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, request
from npc import NPC
import json
import time
import requests

app = Flask(__name__)
npc = NPC()
session = requests.session()


def from_benben(question):
    return None

@app.route('/')
def chat():
    return render_template('index.html')

@app.route('/query')
def query():
    question = request.args.get('question')
    topic = request.args.get('topic')
    res = npc.enquiry(question, topic)
    if res != 'None':
        return res
    else:
        benben_res = from_benben(question)
        if benben_res is None:
            return '我不知道你在说什么啊~'
        else:
            return benben_res

@app.route('/persona')
def get_persona():
    start = time.time()
    topic = request.args.get('topic')
    if topic not in npc.fetcher.persona:
        return None
    else:
        res = npc.fetcher[topic]
    resp = json.dumps(res, ensure_ascii=False, indent=4)
    # return resp
    return resp.replace('\n', '</br>').replace(' ', '&nbsp;')


@app.route('/sessions')
def get_sessions():
    filter_list = ['侯亮平', '令狐冲', '郭靖', '杨过', '张无忌', '乔峰', '萧峰']
    # filter_list = None
    dct = []
    for i, person in enumerate(npc.fetcher.persona):
        if filter_list is None or person in filter_list:
            session = {'id': i,
                       'user': {'name': person,
                                'img': '/static/dist/images/zh%02d.jpg'%(i % 9 + 1)},
                       'messages': [{'content': '你好，我是%s~'% person, 'date': 'null'}]
                       }
            dct.append(session)
    for i, person in enumerate(npc.fetcher.persona):
        if filter_list is None or person not in filter_list:
            session = {'id': i,
                       'user': {'name': person,
                                'img': '/static/dist/images/zh%02d.jpg'%(i % 9 + 1)},
                       'messages': [{'content': '你好，我是%s~'% person, 'date': 'null'}]
                       }
            dct.append(session)
    return json.dumps(dct, ensure_ascii=False)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 80)

