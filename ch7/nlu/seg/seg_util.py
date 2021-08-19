# -*- coding: utf-8 -*-
"""
分词
"""
from ch7.nlu.seg.jieba_util import jieba_util
from ch7.nlu.seg.ltp_util import ltp_seg_handler

# 加载同义词字典
stopwords_set = set()
stopwords_set.add('')
stopwords_set.add(' ')
with open('data/stopwords.txt', 'r') as f:
    lines_list = f.readlines()
    for line in lines_list:
        stopwords_set.add(line.strip())


def jieba_cut(sent, filter_stopword=False):
    """
    结巴分词实现
    :param sent: 分词输入语句
    :param filter_stopword: 是否过滤停用词
    :return: 分词结果列表
    """
    fin_list = []
    seg_list = jieba_util.jieba_cut(sent)
    for word in seg_list:
        if filter_stopword:
            if word not in stopwords_set:
                fin_list.append(word)
        else:
            fin_list.append(word)
    return fin_list


def ltp_cut(sent, filter_stopword=False):
    """
    ltp分词实现
    :param sent: 分词输入语句
    :param filter_stopword: 是否过滤停用词
    :return: 分词结果列表
    """
    fin_list = []
    seg_list = ltp_seg_handler.segment(sent)
    for word in seg_list:
        if filter_stopword:
            if word not in stopwords_set:
                fin_list.append(word)
        else:
            fin_list.append(word)
    return fin_list
