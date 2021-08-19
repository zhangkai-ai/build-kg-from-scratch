#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
话题抽取
"""

from ch7.nlu.intent_classification import predict
from ch7.nlu.seg.ltp_util import ltp_seg_handler
from ch7.util.trie_match import TrieTree

MODEL_DIR = "model.bin"  # 分类模型路径
KG_TREE = TrieTree()  # 字典树
KG_TREE.load("entity.marisa")  # 加载字典树数据


def classify_topic(sent):
    """
    话题分类功能函数，分类器可自行替换，示例采用fasttext，模型训练方式详见ch7/nlu/intent_classification.py
    :param sent: 输入文本
    :return: 话题列表
    """
    topic_list = []
    # 分词
    seg_list = ltp_seg_handler.segment(sent)
    # 预测句子list的结果
    top_preds = predict(seg_list, MODEL_DIR, 3)
    for y_pred, y_prob in top_preds:
        topic_list.append(y_pred)
    return topic_list


def main_part_extractor(sent):
    """
    基于主成分提取的话题抽取功能函数
    :param sent: 输入文本
    :return: 话题列表
    """
    candidate_set = set()
    tag_list = get_pos_tag(sent)
    for candidate, tag in tag_list:
        if tag in ['n', 'j', 'v']:
            candidate_set.add(candidate)
    main_part_set = set()

    # trie树匹配实体词汇
    matched_list = KG_TREE.trie_match(sent)
    for candidate in matched_list:
        if candidate in candidate_set:
            main_part_set.add(candidate)
    return main_part_set


def get_pos_tag(sent):
    """
    获取词性标注
    :param sent: 输入文本
    :return: 词性标注结果
    """
    seg_list = ltp_seg_handler.segment(sent)
    tag_list = ltp_seg_handler.pos_tag(sent)
    return zip(seg_list, tag_list)
