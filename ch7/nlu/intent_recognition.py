#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
意图识别
"""

import re
from nlu.intent_classification import predict

ques_expr_reg = re.compile("什么|啥|多少|何|怎么|怎样|吗|哪|谁|什么地方" \
                           "|多大|多高|多细" \
                           "|几月|几号|几岁|几种" \
                           "|是男是女|好不好|是不是" \
                           "|(是.+还是.+)")

hello_intent_reg = re.compile('你好|hello|hi|早上好|中午好|晚上好')


def full_match(sent):
    """
    全匹配意图识别方法
    :param sent: 输入语句
    :return: 意图
    """
    intent = ''
    if sent == '你好':
        intent = 'hello'
    if sent == '姚明的身高是多少？':
        intent = 'qa'

    return intent


def reg_match(sent):
    """
    基于正则模板的意图识别方法
    :param sent: 输入语句
    :return: 意图
    """
    intent = ''
    if ques_expr_reg.search(sent):
        intent = 'qa'
    elif hello_intent_reg.search(sent):
        intent = 'hello'
    else:
        intent = 'chat'
    return intent


def model_match(sent, model_path, topN=3):
    """
    基于模型的意图识别方法
    :param sent: 输入语句
    :param model_path: 模型路径
    :param topN: 返回N个最高得分结果
    :return: 意图
    """
    intent = predict([sent], model_path, topN=topN)
    return intent

