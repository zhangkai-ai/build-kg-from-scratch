#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
@author  : Winnie
@contact : li_fangyuan@gowild.cn
@time    : 2020/7/20 上午1:01
@description: 

'''
import re

def get_slot_variable(text):
    # 提取出模板中包含的所有变量信息
    regex = '\(([a-zA-Z_]+)\)'
    m = re.findall(regex, text)
    return m

def nlg_template_filling(template, triple, special_reply):
    '''
    nlg回复生成
    :param template: 输入的答句模板
    :param triple: 提取的三元组信息
    :param special_reply: 自定义个性化话术
    :return: nlg回复
    '''
    # 获取模板中所有的槽位变量
    answer = template
    slot_variables = get_slot_variable(template)
    for var in slot_variables:
        # 填入三元组信息
        if var in triple:
            answer = answer.replace('(' + var + ')', triple[var])
        # 填入个性化话术
        elif var in special_reply:
            answer = answer.replace('(' + var + ')', special_reply[var])
        else:
            answer = answer.replace('(' + var + ')', '')

    return answer