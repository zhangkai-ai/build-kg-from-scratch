#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
@author  : Winnie
@contact : li_fangyuan@gowild.cn
@time    : 2020/7/13 上午12:45
@description: 

'''
import re
import time
import json
import random
from util.tools import util
# from data_access import kg_service
from util.trie_match import entity_trie
from relation_extraction import relation_extractor
from template_match.reg_util import attributes_dict

attributes_rever_dict = {} # 全部属性倒排
for key in attributes_dict: #全部属性列表
    attributes_rever_dict[attributes_dict[key]] = key


def handler(sent_seg, user_id, intent, dst):
    sent = sent_seg.replace(' ', '')
    start_time = time.time()

    reply = None
    # actions = {}
    # rst_list = None
    subject_slot = None
    # old_subject_slot = None
    predicate_slot = None
    # old_predicate_slot = None
    object_slot = None
    # old_object_slot = None
    # load dst slots
    # if dst:
    #     if 'subject' in dst:
    #         old_subject_slot = dst['subject']
    #     if 'predicate' in dst:
    #         old_predicate_slot = dst['predicate']
    # print('dst(old) slots: {}, {}'.format(old_subject_slot, old_predicate_slot))

    # extract slots
    # try:
    if True:
        triple_list = relation_extractor.triple_extract(sent)
        print(triple_list)
        if triple_list:
            triple = triple_list[0]
            subject_slot = triple['subject']
            if triple['predicate'] in attributes_rever_dict:
                predicate_slot = attributes_rever_dict[triple['predicate']]
            else:
                predicate_slot = triple['predicate']
            if 'object' in triple:
                object_slot = triple['object']
            else:
                object_slot = "x?"
            if len(predicate_slot) == 1:
                predicate_slot = None
        print('extracted slots: {}, {}, {}'.format(subject_slot, predicate_slot, object_slot))

        # if len(triple_list) != 0:
        #     if "subject_jump:" in object_slot:
        #         object_slot_new = object_slot.replace("subject_jump:","")
        #         subject_slot_new = subject_slot + "的" + object_slot_new
        #         print('subject_slot_new', subject_slot_new)
        #         if sent.find(subject_slot_new) != -1:
        #             matched_dict_subject = entity_tree.trie_match(subject_slot_new)
        #             print('matched_dict_subject', matched_dict_subject)
        #             if subject_slot_new in matched_dict_subject:
        #                 subject_slot = subject_slot_new
        #                 object_slot = "x?"

        # logic functions
        # print('new_extracted slots: {}, {}, {}'.format(subject_slot, predicate_slot, object_slot))
        if subject_slot and predicate_slot and object_slot:
            # print subject_slot, predicate_slot, object_slot
            rst_list = triple_list[1]
            # rst_list = kg_service.search_object_service_fuzzy(subject_slot, predicate_slot, object_slot)
            # end_time = time.time()
            if len(rst_list) != 0:
                candidate_list = []
                slots = {'subject': subject_slot, 'predicate': predicate_slot, 'object': object_slot}
                if object_slot == "x?":
                    for candidate_dict in rst_list:
                        content = candidate_dict['candidate_list']
                        disambiguation = candidate_dict['disambiguation']
                        if predicate_slot == 'abstract':
                            content_str = '{}，'.format(subject_slot)
                        else:
                            nlg_list = [
                                '',
                                '答案是'
                            ]
                            content_str = nlg_list[random.randint(0, len(nlg_list) - 1)]
                        content_new = content
                        content = set()
                        for content_cell in content_new:
                            content.add(content_cell)
                        if len(content) <= 3:
                            for part in content:
                                content_str += (part + '，')
                            content_str = content_str[:-1]
                        else:
                            content = list(content)
                            content_str = content_str + '{}, {}, {}等'.format(content[0], content[1], content[2])
                        candidate_list.append({'content': content_str, 'disambiguation': disambiguation})
                    if len(candidate_list) == 1:
                        actions = {'content': candidate_list[0]['content']}
                        reply = {'slots': slots, 'actions': actions}
                    else:
                        disambiguation_str = candidate_list[0]['content']
                       # actions = {'content': disambiguation_str, 'candidates': candidate_list, 'next_intent': 'query'}
                        actions = {'content': disambiguation_str}
                       # reply = {'slots': slots, 'actions': actions, 'intent': 'ask_select'}
                        reply = {'slots': slots, 'actions': actions}
                else:
                    if "bool_compare" in rst_list[0]:
                        compare_how_more = u"更?大|更?宽|更?长|更?高|更?重|更?晚|更?多"
                        compare_how_less = u"更?小|更?窄|更?短|更?矮|更?轻|更?早|更?少|更?低"

                        regex_more = re.search(compare_how_more, sent)
                        regex_less = re.search(compare_how_less, sent)
                        if regex_more:
                            suffix = regex_more.group()
                        if regex_less:
                            suffix = regex_less.group()
                            tmp_slot = subject_slot
                            subject_slot = object_slot
                            object_slot = tmp_slot
                        if rst_list[0]['bool_compare'] == True:
                            subject_slot = subject_slot.replace("subject_compare:","")
                            disambiguation_str = "{}{}".format(subject_slot, suffix)
                        elif(rst_list[0]['bool_compare'] == "Same"):
                            disambiguation_str = "一样"
                        else:
                            object_slot = object_slot.replace("subject_compare:","")
                            disambiguation_str = "{}{}".format(object_slot, suffix)
                        #actions = {'content':disambiguation_str, 'candidates':candidate_list, 'next_intent':'query'}
                        #reply = {'slots':slots, 'actions':actions, 'intent':'ask_select'}
                        actions = {'content':disambiguation_str}
                        reply = {'slots':slots, 'actions':actions}
                    else:
                        # 实体出现歧义，进行问询
                        for candidate_dict in rst_list:
                            content = candidate_dict['candidate_list']
                            disambiguation = candidate_dict['disambiguation']
                            object_label = candidate_dict.get('object_label','x?')
                            content_str = ""
                            for content_cell in content:
                                content_str = content_str + content_cell + ','
                            content_str = content_str.strip(',')
                            disambiguation_str = ''
                            if content_str == "":
                                disambiguation_str = kg_service.get_cqa_answer(sent.decode("utf-8"))
                            else:
                                disambiguation_str = "答案是{}".format(content_str)
                            # if object_label == 'yes':
                            #     disambiguation_str = "您的答案是正确的"
                            # else:
                            #     if content_str == "":
                            #         disambiguation_str = kg_service.get_cqa_answer(sent.decode("utf-8"))
                            #         # disambiguation_str = "抱歉， 我也不知道这个问题的答案， 我会继续努力的"
                            #     else:
                            #         disambiguation_str = "正确的答案应该是{}".format(content_str)
                            actions = {'content': disambiguation_str, 'candidates': candidate_list, 'next_intent': 'query'}
                            reply = {'slots': slots, 'actions': actions, 'intent':'ask_select'}
            else:
                actions = {'content': ''}
        else:
            actions = {'content': ''}
    # except Exception as e:
    #     # print(e)
    #     # actions = {'content':"抱歉，我不知道这个问题的答案，我会继续努力的"}
    #     actions = {'content': ''}
    # print('kg cost: {}'.format(time.time() - start_time))
    # start_time = time.time()
    # if not actions.get('content', ''):
    #     # 问句判断
    #     if ques_expr_reg.search(sent):
    #         cqa_rst, source = cqa_handler.cqa_general_handler(sent.decode("utf-8"))
    #         actions = {'content': cqa_rst, 'source': source}
    #     reply = {'actions': actions}
    # else:
    #     reply['actions']['source'] = 'kg'
    # print('cqa cost: {}'.format(time.time() - start_time))
    return json.dumps(reply, ensure_ascii=False)


if __name__ == '__main__':
    test_case_list = [
    #     # 特殊疑问句
    #     '周杰伦的星座是什么',
    #     '哪里是阿里巴巴的总部地点',
    #     '你知道美人鱼的导演吗',
    #     '请回答我三国演义是谁写的',
    #     '曾国藩家书是什么时候出版的',
    #     # 一般疑问句
    #     '薛之谦的血型是o型吗',
    #     '围城的出版时间是1948年吗',
    #     '682是依云小镇的总户数？',
    #     '周杰伦的出生时间是1993年12月29号吗',
    #     '国有企业是中兴通讯股份有限公司的企业类型吗',
    #     # 比较句式
    #     '上海和江苏哪个面积更大',
    #     '马云和马化腾相比谁的出生日期更早',
    #     '范志毅和刘敏相比谁的学历更低',
    #     '华谊兄弟传媒集团和EXO相比谁的成立时间更早',
    #     '美国和俄罗斯相比哪个国家的国土面积更大',
    #     # 上下位句式
    #     '周杰伦的代表作品中属于流行音乐的是什么',
    #     '上海的著名景点中属于公园的是什么',
    #     '复旦大学的知名校友中是政治学家的有谁',
    #     '霸王别姬的主演中属于歌手的有谁',
    #     # 推理句式
    #     '美人鱼的导演的主要成就是什么',
    #     '谢贤的儿子的妈妈是谁',
    #     '十全武功的相关人物的所处时代是什么',
    #     '陈忠实的作品的页数是多少',
    #     '阿里巴巴的创始人的国籍是什么',
    #     # 摘要句式
    #     '什么是比特币',
    #     '李达康是谁',
    #     '图灵测试是什么',
    #     # 兜底句式
    #     '天空为什么是蓝的',
    #     '龙虾怎么剥',
    #     '狗能吃芒果吗',
    #     '周杰伦的身高',
    #     '马云的国籍',
    #     '马云和马化腾谁年龄大',
    #     '美人鱼的导演的主要成就是什么',
    #     '周杰伦的星座是摩羯座吗？',
    #     '围城的出版时间是十八年吗',
    #     '三体的出版时间是今年吗'
    #
    # ]
        '美人鱼的导演的主要成就是什么']
    for s in test_case_list:
    # s = '美人鱼的导演的主要成就是什么'#'周杰伦的代表作品中属于流行音乐的是哪些'#'周杰伦的身高是多少'

        handler(s, '111', '', '')