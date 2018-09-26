# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import rstr
import random
import os


class RelationAnswer:
    def __init__(self):
        self.temp1 = u'(我(的|)REL|)(是|叫)ENT(啊|)(~|!|)'
        self.temp2 = u'(我(的|)REL|)是(PRO|)ENT(~|!|)'
        self.temp3 = u'(我(的|))REL是ENT, GENDER是PRO(呢|)(~|!|)'
        self.temp4 = u'(我(的|)REL|)有ENT(~|!|)'
        self.titles = {u'职位', u'职务', u'职称', u'称号', u'身份'}

    def gen_answer(self, persona, rel, fact):
        if isinstance(fact, str) and fact in persona:
            persona = persona[fact]
            titles = self.titles & set(persona['prop'].keys())
            if u'性别' in persona['prop'] and len(titles) > 0 and random.randint(0, 1) == 0:
                title = titles.pop()
                resp = rstr.xeger(self.temp3)
                # print(rel, fact, persona['prop'][title])
                title = persona['prop'][title]
                if isinstance(title, list):
                    random.shuffle(title)
                    title = title[0]
                resp = resp.replace('REL', rel).replace('ENT', fact).replace('PRO', title)
                if persona['prop'][u'性别'] == '女':
                    resp = resp.replace('GENDER', u'她')
                else:
                    resp = resp.replace('GENDER', u'他')
                return resp
            elif len(titles) > 0:
                title = titles.pop()
                if isinstance(title, list):
                    random.shuffle(title)
                    title = title[0]
                resp = rstr.xeger(self.temp2)
                resp = resp.replace('REL', rel).replace('ENT', fact).replace('PRO', persona['prop'][title])
                return resp
        elif isinstance(fact, list):
            resp = rstr.xeger(self.temp4).replace('ENT', '、'.join(fact)).replace('REL', rel)
            return resp
        else:
            resp = rstr.xeger(self.temp1)
            resp = resp.replace('REL', rel).replace('ENT', fact)
            return resp

class ProfileAnswer:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.template_file = self.path + '../dicts/template.txt'
        self.syn_file = self.path + '../dicts/syn_dict'
        self.syn_dct = {}
        self.templates = ['']
        self._load_template()
        self.all_temp = u'我的LABEL是FACT'

    def _load_template(self):
        with open(self.template_file) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for line in lines:
                self.templates.append(line)
        with open(self.syn_file) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for i, line in enumerate(lines):
                lst = line.split('|')
                for it in lst:
                    self.syn_dct[it] = i + 1


    def gen_answer(self, persona, label):
        if label not in persona['prop']:
            return None

        fact = persona['prop'][label]
        if isinstance(fact, list) and len(fact) > 0:
            random.shuffle(fact)
            if random.randint(0, 1) == 1:
                fact = fact[0]
            else:
                fact = '、'.join(fact)
        resp = rstr.xeger(self.all_temp).replace('LABEL', label).replace('FACT', fact)

        if label.encode('utf8') not in self.syn_dct:
            return resp
        else:
            id = self.syn_dct[label.encode('utf8')]
            temp = self.templates[id]
            if temp == '':
                return resp
            else:
                temp = rstr.xeger(u'%s' % temp)
                resp = temp.replace('PROP', fact)
                return resp

if __name__ == '__main__':
    relans = RelationAnswer()
    print rstr.xeger(relans.temp3)