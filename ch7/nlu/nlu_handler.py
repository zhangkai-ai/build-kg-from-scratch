#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
nlu处理
"""
from ch7.nlu.seg.seg_util import jieba_cut
from ch7.nlu.intent_recognition import full_match, reg_match
from ch7.util.multi_thread_util import thread_factory


def nlu_main_handler(sent):
    """
    自然语言理解主处理函数
    :param sent: 待nlu的输入语句
    :return: nlu处理结果
    """
    nlu_dict = {
        'input': sent,
        'base_nlu': {},     # 基础nlu结果，分词、词性标注、依存等
        'intent': '',       # 意图识别结果
        'slot': {}          # 通用槽位提取结果
    }

    # 并行执行各个nlu模块
    jieba_cut_task = thread_factory.add_thread(jieba_cut, sent)     # 分词，可替换其他实现
    intent_task = thread_factory.add_thread(full_match, sent)       # 意图识别

    # 1. base nlu
    jieba_cut_rst = thread_factory.get_rst(jieba_cut_task)
    nlu_dict['base_nlu']['jieba_cut'] = jieba_cut_rst

    # 2. intent_recognition
    intent = thread_factory.get_rst(intent_task)
    # 组合意图识别策略
    if not intent:
        intent = reg_match(sent)
    nlu_dict['intent'] = intent

    # 3. nerl

    return nlu_dict

