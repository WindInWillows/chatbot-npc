# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import jieba
import os


class Retriever:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.cilin = self.path + 'cilin.txt'
        self.syn_file = self.path + '../dicts/syn_dict'
        self.cilin_dct = {}
        self.syn_dct = {}
        self.syn_lst = []
        self.load_cilin()

    def load_cilin(self):
        with open(self.cilin) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for i, line in enumerate(lines):
                if ' ' not in line:
                    continue
                val = line.split()[0]
                keys = line.split()[1:]
                for key in keys:
                    self.cilin_dct[key] = val
        with open(self.syn_file) as fin:
            lines = [line.strip() for line in fin.readlines()]
            for i, line in enumerate(lines):
                lst = line.split('|')
                self.syn_lst.append(lst)
                for it in lst:
                    self.syn_dct[it] = i

    def query(self, question, labels):
        # print question, ' '.join(labels)
        qwords = jieba.lcut(question)
        # 标签直接在问题中出现
        for label in labels:
            if label in question:
                return label
            # 在同义词词典中
            if label.encode('utf8') in self.syn_dct:
                lst = self.syn_lst[self.syn_dct[label.encode('utf8')]]
                for it in lst:
                    if it in question:
                        return label

        # 在词林词典中出现
        for qw in qwords:
            if qw.encode('utf-8') in self.cilin_dct:
                for label in labels:
                    if label.encode('utf-8') in self.cilin_dct and self.cilin_dct[label.encode('utf-8')] == self.cilin_dct[qw.encode('utf-8')]:
                        return label
        return None
