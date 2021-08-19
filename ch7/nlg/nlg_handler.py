#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
自然语言生成，即对话回复生成
"""
import random

hello_chat_template = [
    '你好',
    'hi',
    'hello',
    '很高兴见到你'
]

qa_template = [
    '答案是{}',
    '正确答案是{}',
    '{}'
]


def nlg_main_handler(dst, nlu_dict):
    """
    dst为空表明可用服务无返回结果，进入兜底，否则根据不同的service名称，选择nlg模板
    :param dst: dst结果
    :param nlu_dict: nlu执行结果字典
    :return: 添加nlg的最终返回结果
    """
    if dst:
        service = dst["service"]
        if service == "hello_chat":
            nlg = random.choice(hello_chat_template)
        elif service in ["bot_qa", "common_qa", "medicine_qa", "user_qa"]:
            nlg = dst["nlg"]
            # TODO: 待丰富句式
            dst["nlg"] = random.choice(qa_template).format(nlg)
        rst = dst
    else:
        # 兜底安全回复
        rst = {
            "service": "no_service",
            "nlg": "这是兜底回复"
        }
    return rst

