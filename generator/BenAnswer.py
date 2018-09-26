# -*- coding: utf-8 -*-
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import requests

# BEN_API = "http://120.25.81.83/irobot/ask"      # 正式笨笨接口，调试阶段先不要用
# BEN2_API = 'http://bbd.8wss.com/irobot/ask'     # 笨笨小二接口


class BenAnswer:
    def __init__(self):
        self.BEN2_API = 'http://bbd.8wss.com/irobot/ask'

    def answer(self, uid, post):
        paras = {
            'content': post, 
            'uid': uid
        }
        resp = requests.post(self.BEN2_API, json=paras)
        if resp.status_code == 200:
            return resp.json()['answer']
        else:
            return None