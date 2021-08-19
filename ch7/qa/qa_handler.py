#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
问答处理
"""
import configparser
from qa import bot_qa, common_qa, medicine_qa, user_qa

__cf = configparser.ConfigParser()
__cf.read("./config.ini")
url_test = __cf.get("module", "url_test")


def qa_main_handler(sent, user_id, nlu_dict):
    """
    qa主处理函数，按优先级对访问问答接口，通用问答、医药问答、用户信息问答、bot人设问答
    :param sent:
    :param user_id:
    :param nlu_dict:
    :return:
    """
    reply = common_qa.handler(sent, user_id, nlu_dict)
    if not reply:
        reply = medicine_qa.handler(sent, user_id, nlu_dict)
    if not reply:
        reply = user_qa.handler(sent, user_id, nlu_dict)
    if not reply:
        reply = bot_qa.handler(sent, user_id, nlu_dict)
    return reply
