#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
主函数入口
"""
import time
from loguru import logger
from nlu.nlu_handler import nlu_main_handler
from dm.dm_handler import dm_main_handler
from nlg.nlg_handler import nlg_main_handler
from dm.dst_manager import add_dst


def sent_handler(sent, user_id):
    """
    对话输入语句的主处理函数
    :param sent: 对话输入语句
    :param user_id: 用户的id
    :return: 对话回复语句
    """
    # 1. NLU模块，获取对话意图，及通用自然语言理解
    nlu_dict = nlu_main_handler(sent)
    '''
    nlu_dict_example = {
        "input": "xxx",
        "base_nlu": {
            "jieba_cut": ["a", "b"]
        },
        "intent": "qa",
        "slot": {}
    }
    '''
    logger.info("NLU RST: {}".format(str(nlu_dict)))

    # 2. DM模块，对话管理，选择候选服务并调用，结果排序
    dst = dm_main_handler(user_id, nlu_dict)
    logger.info("DM RST: {}".format(str(dst)))

    # 3. NLG模块
    dst = nlg_main_handler(dst, nlu_dict)
    logger.info("NLG RST: {}".format(str(dst)))

    # 4. 保存本轮结果到dst中
    dst["time"] = time.time()
    add_dst(user_id, dst)

    return dst


if __name__ == '__main__':
    # rst = sent_handler('你是谁', 'test002')
    test_case = [
        "周杰伦的星座是什么",
        "那你呢",
        "我的星座是什么",
        "你的星座是什么",
        "PD-1的antibody是什么",
        "奥运会全称是什么",
    ]
    for case in test_case:
        rst = sent_handler(case, 'test_user')
        logger.info("*"*100)
