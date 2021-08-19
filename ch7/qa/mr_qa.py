#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
基于机器阅读理解的问答
参考项目：https://github.com/baidu/DuReader，提供开源数据集及baseline
"""

import requests


def handler(user_id, nlu_dict, dst):
    """
    基于机器阅读理解的问答处理函数，假设调用MR服务
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return:
    """
    text = nlu_dict["input"]
    try:
        body = {
            "question": text
        }
        r = requests.post('http://192.168.1.100:9000', data=json.dumps(body), timeout=2)
        rst = r.json()
        return rst["data"]["answer"]
    except Exception as e:
        return None


