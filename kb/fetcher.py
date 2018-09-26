# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import os

REL = 'rel'
PROP = 'prop'

class Fetcher:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.persona = {}
        for _,_,files in os.walk(self.root_path+'personas/json'):
            for file in files:
                jsn = json.load(open(self.root_path + 'personas/json/%s'%file))
                for name in jsn:
                    if name in self.persona:
                        for key in jsn[name][REL]:
                            if key not in self.persona[name][REL]:
                                self.persona[name][REL][key] = jsn[name][REL][key]
                        for key in jsn[name][PROP]:
                            if key not in self.persona[name][PROP]:
                                self.persona[name][PROP][key] = jsn[name][PROP][key]
                        # self.persona[name][REL] = {**self.persona[name][REL], **jsn[name][REL]}
                        # self.persona[name][PROP] = {**self.persona[name][PROP], **jsn[name][PROP]}
                    else:
                        self.persona[name] = jsn[name]

    def __getitem__(self, item):
        if u'%s'%item not in self.persona:
            return None
        # assert item in self.persona, 'key not in dict'
        return self.persona[u'%s' % item]

if __name__ == '__main__':
    fetcher = Fetcher()
    print(fetcher["郭靖"])
