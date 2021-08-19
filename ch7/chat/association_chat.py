#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
联想功能，详情参考6.4小节
"""
from association.main_handler import handler


def handler(user_id, nlu_dict, dst):
    """
    联想闲聊处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return:
    """
    text = nlu_dict["input"]
    rst = None
    ans = handler(text, user_id)
    if ans:
        # 组装返回结果
        rst = {
            "service": "association_chat.py",
            "nlg": ans
        }
    return rst
