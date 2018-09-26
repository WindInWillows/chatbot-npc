# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from kb.fetcher import Fetcher
from generator.TemplateAnswer import RelationAnswer,ProfileAnswer
from generator.SpAnswer import SPAnswer
from generator.BackAnswer import BackAnswer


class NPC:
    def __init__(self):
        self.fetcher = Fetcher()
        self.cnn_enquirer = None
        self.rel_answer = RelationAnswer()
        self.prop_answer = ProfileAnswer()

        from retrieval.Retriever import Retriever
        self.retriever = Retriever()
        from generator.BiRelAnswer import BiRelAnswer
        self.birel_answer = BiRelAnswer()
        self.sp_answer = SPAnswer()
        self.back_answer = BackAnswer()

    '''
        过滤函数，去掉一些不是属性问答的问题
    '''
    def filt(self, question, topic):
        if u'文摘' in question or u'摘要' in question:
            return True
        # 找不到人物则交给文摘模块处理，返回'None'
        persona = self.fetcher[topic]
        if persona is None:
            return True


    '''
    主函数：
        input: question, topic(人物), novel(小说名)
        output: resp(回复的字符串)
    '''
    def enquiry(self, question, topic, novel=None):
        try:
        # if True:
            persona = self.fetcher[topic]
            if self.filt(question, topic):
                print '###被过滤掉'
                return 'None'
            labels = list(tuple(persona['rel'].keys()) + tuple(persona['prop'].keys()))

            # 先检查是不是需要特殊处理的回答
            resp = self.sp_answer.answer(question, topic, self.fetcher.persona)
            if resp is not None:
                print '###启动特殊回答：', resp
                return resp

            '''
            检索相关fact：
                1. 优先使用检索方法获取标签
                2. 若检索无果则使用CNN进行分类得到近似属性标签，再使用近似标签与候选属性标签匹配得到最相关的候选属性标签
                3. 如果两种方法都找不到合适标签，则交给文摘处理，接口返回'None'
            '''
            label = self.retriever.query(question, labels)
            if label is None:
                # 首先判断是不是询问两人关系
                resp = self.birel_answer.answer(question, topic, self.fetcher.persona)
                if resp is not None:
                    print '###回答两人关系：', resp
                    return resp
                else:
                    resp = self.back_answer.answer(question, topic, persona)
                    if resp is not None:
                        print '###后处理回答：', resp
                        return resp
                    else:
                        return 'None'

            # 检索到的属性值
            fact = persona['rel'][label] if label in persona['rel'] else persona['prop'][label]
            # print 'fact is %s' % fact
            print 'fact:', fact
            '''
            关系回复生成：
                对于人物关系，优先使用模板生成答案句，对于人物属性，先使用常用属性模板回答，
                无法回答则使用Seq2Seq直接生成含有<POS>标签的答案句，再使用相关属性值填充
            '''
            if label in persona['rel']:
                resp = self.rel_answer.gen_answer(self.fetcher.persona, label, fact)
                # print 'template resp: %s' % resp
                # logger.info('answer by template: %s\n' % resp)
                print '###回答人物关系：', resp
                return resp
            else:
                resp = self.prop_answer.gen_answer(persona, label)
                # print 'prop template resp:', resp
                if resp is not None:
                    print '###回答人物属性：', resp
                    return resp
                # Seq2Pos生成
                else:
                    return 'None'
        except:
            print '###Something Error!'
            return 'None'


if __name__ == '__main__':
    npc = NPC()
    test = [
        {'question': u'你和张翠山是什么关系？', 'topic': u'张无忌'},
        {'question': u'来个文摘', 'topic': u'令狐冲'},
        {'question': u'介绍介绍你自己？', 'topic': u'令狐冲'},
        {'question': u'你的老婆是谁？', 'topic': u'萧峰'},
        {'question': u'你小名叫什么？', 'topic': u'令狐冲'},
        {'question': u'你最爱的人是？', 'topic': u'令狐冲'},
        {'question': u'哈哈哈', 'topic': u'郭靖'},
        {'question': u'盖茨比', 'topic': u'郭靖'},
        {'question': u'你会什么武功？', 'topic': u'令狐冲'},
        {'question': u'虚竹的本质是复读机吗', 'topic': u'虚竹'},
    ]
    import time
    for it in test:
        print 'Q:', it['topic'], it['question']
        print 'A:', npc.enquiry(**it)
        time.sleep(1)