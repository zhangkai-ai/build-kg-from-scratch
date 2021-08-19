#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
打招呼功能
"""


def handler(user_id, nlu_dict, dst):
    """
    打招呼处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return:
    """
    # 组装返回结果
    rst = {
        "service": "hello_chat"
    }
    return rst

