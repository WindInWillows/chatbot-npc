# -*- coding: utf-8 -*-
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

import rstr

class BiRelAnswer:
    def __init__(self):
        self.temp1 = u'(GENDER|NAME)是我的REL(，你要找(GENDER)？|，你找(GENDER)(有什么事儿吗|做什么|)？)'
        self.temp2 = u'我是(GENDER|NAME)的REL(，你要找(GENDER)？|，你找(GENDER)(有什么事儿吗|做什么|)？)'
        self.temp3 = u'(|不好意思，|咦，)我好像不认识NAME啊|(|嗯？|咦？|啊哈？)想不起来了，NAME是谁？|(|你别说，|咦，)这个名字还真熟悉，(|让|容)我想想~'
        self.self_qulst = [u'认识SELF', u'知道SELF', u'SELF是谁', u'SELF是你']
        self.temp4 = u'(|哼|我去|额|啊)，你不认识我还跟我聊天|(伤心，|桑心，|)原来你都不认识我的。。。'

    def filt_self(self, question, topic):
        if topic not in question:
            return None
        question = question.replace(topic, 'SELF')
        for it in self.self_qulst:
            if it in question:
                return rstr.xeger(self.temp4)

    '''
        判断问句中是否出现小说中的人物
    '''
    def answer(self, question, topic, persona):
        resp = self.filt_self(question, topic)
        if resp is not None:
            return resp
        for name in persona:
            if name != topic and name in question:
                for key in persona[u'%s'%name]['rel']:
                    if topic in persona[u'%s'%name]['rel'][key]:
                        resp = rstr.xeger(self.temp2)
                        resp = resp.replace('REL', key)
                        if u'性别' in persona[u'%s' % name]['prop']:
                            if persona[u'%s'%name]['prop'][u'性别'] == '女':
                                resp = resp.replace('GENDER', u'她')
                            else:
                                resp = resp.replace('GENDER', u'他')
                        else:
                            resp = resp.replace('GENDER', 'NAME')
                        resp = resp.replace('NAME', name)
                        return resp
                for key in persona[u'%s'%topic]['rel']:
                    if name in persona[u'%s'%topic]['rel'][key]:
                        resp = rstr.xeger(self.temp1)
                        resp = resp.replace('REL', key)
                        if u'性别' in persona[u'%s'%name]['prop']:
                            if persona[u'%s'%name]['prop'][u'性别'] == '女':
                                resp = resp.replace('GENDER', u'她')
                            else:
                                resp = resp.replace('GENDER', u'他')
                        else:
                            resp = resp.replace('GENDER', 'NAME')
                        resp = resp.replace('NAME', name)
                        return resp
                resp = rstr.xeger(self.temp3).replace('NAME', name)
                return resp

        return None