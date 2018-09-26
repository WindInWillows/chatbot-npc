# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import rstr


'''
    简单处理一些属性值
'''
class BackAnswer:
    def __init__(self):
        self.stop_words = []
        self.rel_temp = u''
        self.prop_temp = u'KEY：VAL'

    def answer(self, question, topic, persona):
        topic = u'%s'%topic
        rels = persona['rel'].items()
        props = persona['prop'].items()
        resp = None
        for tp in props + rels:
            key = tp[0]
            val = tp[1]
            if isinstance(val, list):
                for it in val:
                    if it in question:
                        resp = self.prop_temp.replace('KEY', key).replace('VAL', it)
            elif val in question:
                resp = self.prop_temp.replace('KEY', key).replace('VAL', val)
        return resp
