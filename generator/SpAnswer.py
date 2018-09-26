# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import rstr
import re
from retrieval.Retriever import Retriever


'''
    姓氏查询
'''
class LastNameAnswer:
    def __init__(self):
        self.pat = [u'你姓什么', u'姓氏', u'姓啥', u'姓？']
        self.fx_lst = []
        self.dx_lst = []
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/../dicts/'
        self.fx_file = self.path + 'fx.txt'
        self.dx_file = self.path + 'dx.txt'
        with open(self.fx_file) as fin:
            self.fx_lst = [line.strip() for line in fin.readlines()]
        with open(self.dx_file) as fin:
            self.dx_lst = [line.strip() for line in fin.readlines()]
        self.temp1 = u'(我|本人)姓LNAME(名FNAME|)'
        self.temp2 = u'(我叫ANAME，|)(大概|应该|我猜)是姓LNAME吧~'
        self.temp3 = u'我姓LNAME'

    def answer(self, question, topic, persona):
        if topic[:2] in self.fx_lst:
            lname = topic[:2]
            fname = topic[2:]
        elif topic[:1] in self.dx_lst:
            lname = topic[:1]
            fname = topic[1:]
        else:
            lname = topic[:1]
            fname = None

        # 处理姓氏询问
        for it in self.pat:
            if it in question:
                if fname is not None:
                    resp = rstr.xeger(self.temp1).replace('LNAME', lname).replace('FNAME', fname)
                else:
                    resp = rstr.xeger(self.temp2).replace('ANAME', topic).replace('LNAME', lname)
                return resp

        # 处理诸如：“你姓赵吗？”之类的问题
        if u'姓%s'%lname in question:
            return u'对，我姓%s'%lname
        return None


'''
    特殊处理“你是谁”之类的问题
'''
class NameAnswer:
    def __init__(self):
        self.pat = u'(你|您)(是(谁|哪个|哪位|)|的名字|叫(什么|啥|)|谁(啊|)|哪位)(\?|？|)'
        self.pats = set()
        for i in range(500):
            self.pats.add(rstr.xeger(self.pat))
        self.temp = u'你都不认识我NAME了？|你不认识我还跟我聊天，我是NAME|我是NAME|我NAME不想跟你说话，并向你扔了一只狗|我看你是在为难我NAME'

    def answer(self, question, topic, persona):
        if question not in self.pats:
            return None
        else:
            return rstr.xeger(self.temp).replace('NAME', topic)

'''
    处理数量询问的问题
'''
class CountAnswer:
    def __init__(self):
        self.pat = [u'有几个', u'有多少', u'几种']
        self.temp1 = u'有LIST，你自己数吧|有LIST，COUNT个吧'
        self.temp2 = u'只有FACT一个'
        self.retr = Retriever()

    def answer(self, question, topic, persona):
        persona = persona[topic]
        for it in self.pat:
            if it in question:
                labels = list(tuple(persona[u'rel'].keys()) + tuple(persona[u'prop'].keys()))
                label = self.retr.query(question, labels)
                if label is None:
                    return None
                fact = persona['rel'][label] if label in persona['rel'] else persona['prop'][label]
                if isinstance(fact, list) and len(fact) > 0:
                    resp = rstr.xeger(self.temp1).replace('LIST', '、'.join(fact)).replace('COUNT', str(len(fact)))
                    print resp
                    return resp
                elif isinstance(fact, str):
                    resp = rstr.xeger(self.temp2).replace('FACT', fact)
                    return resp
        return None

'''
    一些需要特殊处理的回答，包括：
    1. 姓氏回答
    2. 数量回答
    3. 关于“你是谁”等的基础回答
'''
class SPAnswer:
    def __init__(self):
        self.ln_answer = LastNameAnswer()
        self.name_answer = NameAnswer()
        self.count_answer = CountAnswer()

    def answer(self, question, topic, persona):
        topic = u'%s'%topic
        resp = self.ln_answer.answer(question, topic, persona)
        if resp is not None:
            return resp
        resp = self.name_answer.answer(question, topic, persona)
        if resp is not None:
            return resp
        resp = self.count_answer.answer(question, topic, persona)
        if resp is not None:
            return resp

