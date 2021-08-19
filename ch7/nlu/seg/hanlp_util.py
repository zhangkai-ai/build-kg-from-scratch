#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
HanLP分词
"""
from pyhanlp import HanLP, JClass

# pyhanlp配置
HanLP.Config.ShowTermNature = False
# crf分词器
crf_seg = HanLP.newSegment("crf")
# 感知机分词器
perceptron_seg = HanLP.newSegment("perceptron")
# n最短路径分词器
nshort_seg = HanLP.newSegment("nshort")
# 维特比算法分词器
viterb = HanLP.newSegment("viterbi")
# 极速分词器，采用双数组trie树分词算法
bi_trie = HanLP.newSegment("dat")
# 基础分词器
basic_tokenzier = JClass("com.hankcs.hanlp.tokenizer.BasicTokenizer")
# 标准分词器
standard_tokenizer = JClass("com.hankcs.hanlp.tokenizer.StandardTokenizer")
# n最短路径分词器另一种调用方法，模型版本有所不同，分词结果略有不同
NShortSegment = JClass("com.hankcs.hanlp.seg.NShort.NShortSegment")
nshort_segment = NShortSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)
# 最短路径算法分词器
ViterbiSegment = JClass("com.hankcs.hanlp.seg.Viterbi.ViterbiSegment")
shortest_segment = ViterbiSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)


# pyhanlp的几种模式
def hanlp_default(s):
    # 标准分词器：维特比分词器, 与viterbi分词器结果一致
    res = HanLP.segment(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_basic(s):
    # 基础分词器
    res = basic_tokenzier.segment(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_crf(s):
    # crf分词器
    res = crf_seg.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_perceptron(s):
    # 感知机分词器
    res = perceptron_seg.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_nshort1(s):
    # n最短路径分词器
    res = nshort_seg.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_nshort2(s):
    # n最短路径分词器另一种调用方法，与hanlp_nshort1结果略有不同
    res = nshort_segment.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_shortest(s):
    # 最短路径算法分词器
    res = shortest_segment.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_viterbi(s):
    # 维特比算法分词器
    res = viterb.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)

def hanlp_bitrie(s):
    # 双数组trie树分词器
    res = bi_trie.seg(s)
    words = [term.word for term in res]
    return ' '.join(words)


