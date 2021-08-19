#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
基于检索的问答
"""
from util.es_util import es_object
from util.hnsw_util import hnsw_object


# 示例检索库
ir_base = {
    "奥运会全称是什么": "奥林匹克运动会",
    "愚人节在几月几日": "四月一日",
    "焚书坑儒是谁干的": "秦始皇"
}


def handler(user_id, nlu_dict, dst, match_mode="full"):
    """
    基于检索的问答处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :param match_mode: 匹配支持三种方式，"full"全串匹配、"es"基于es的字符相似度匹配、"embedding"基于embedding的向量相似度匹配
    :return:
    """
    text = nlu_dict["input"]
    rst = None
    match = None

    if match_mode == "full":
        match = ir_base.get(text, None)
    elif match_mode == "es":
        match = match_by_es(text)
    elif match_mode == "embedding":
        match = match_by_embedding(text)
    if match:
        rst = {
            "service": "ir_qa",
            "nlg": match
        }
    return rst


def match_by_es(text):
    """
    基于字符相似度进行检索，利用es默认的BM25算法进行knn查询
    :param text: 待匹配文本
    :return: 匹配上的文本
    """
    match_list = es_object.query(text, "ir_base")
    if match_list:
        return match_list[0]
    else:
        return None


# 构建hnsw检索库
# hnsw_object.insert(ir_base.keys(), ir_base.values())

def match_by_embedding(text):
    """
    基于embedding相似度进行检索，利用hnsw进行knn查询加速
    :param text: 待匹配文本
    :return: 匹配上的文本
    """
    labels, distance = hnsw_object.query(text)
    if labels:
        return labels[0]
    else:
        return None
