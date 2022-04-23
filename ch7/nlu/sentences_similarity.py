#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
文本相似度
"""

import difflib
from fuzzywuzzy import fuzz
from nlu.seg.ltp_util import LTPHander, LTP_PATH

# 创建一个ltp工具类的对象，任务类型传参为词性标注postag
ltp = LTPHander(LTP_PATH, task_type='postag')

# 方法1
def similarity(sent1, sent2):
    """
    difflib包计算序列相似度的方法
    :param sent1:
    :param sent2:
    :return: 返回的是0-1之间的相似概率，0为完全不相似，1为完全相同
    """
    score = difflib.SequenceMatcher(None, sent1, sent2).ratio()
    return score


# 方法2
def fuzz_similarity(sent1, sent2):
    """
    fuzzy包计算序列相似度的方法
    :param sent1:
    :param sent2:
    :return: 返回的是百分制的分值，0为完全不相似，100为完全相同
    """
    return fuzz.ratio(sent1, sent2)


def weighted_match_similarity(sent1, sent2, w1=None, w2=None):
    """
    计算两个字符串的加权相似度
    :param sent1:
    :param sent2:
    :param w1: w1是一个与sent1长度相同的权重序列
    :param w2: w2是一个与sent2长度相同的权重序列
    :return:
    """
    mb = difflib.SequenceMatcher(None, sent1, sent2).get_matching_blocks()
    if not w1 and not w2:  # 如果均不加权重
        matches = sum(triple[-1] for triple in mb)
        return calculate_ratio(matches, len(sent1) + len(sent2))

    else:
        if not w1:
            w1 = len(sent1) * [1.0]
        if not w2:
            w2 = len(sent2) * [1.0]
        # 校验权重序列是否和字符串等长
        assert len(sent1)==len(w1)
        assert len(sent2)==len(w2)

        matches = sum((w1[tri[0] + i] + w2[tri[1] + i]) / 2 for tri in mb for i in range(tri[-1]))

        return calculate_ratio(matches, sum(w1) + sum(w2))


def calculate_ratio(matches, length):
    if length:
        return 2.0 * matches / length
    return 1.0


def get_weight(sent):
    w_l = []
    w_map = {
        'v': 1.0,
        'r': 0.5,
        'd': 0.4
    } # 暂时根据词性设定的一个权重表，可以优化，比如设定一些特定的否定词权重高一点等
    pos1 = ltp.pos_tag(sent)
    for w in pos1:
        w_l.extend(len(w[0]) * [w[1]])

    w_l = [w_map[w] for w in w_l]
    return w_l


if __name__ == '__main__':
    s1 = '我喜欢你'
    s2 = '我不喜欢你'
    s3 = '我喜欢你呀'

    '''
    1、基于公共子串计算的相似度方法，每个字的权重相同，有两种写法
    '''
    print(similarity(s1, s2))
    print(fuzz_similarity(s1, s2))

    '''
    2、加权的文本相似度匹配方法
    # 下面为了测试方便，指定一组权重值列表，读者在实际应用时，可以从两种思路出发设置权重：
    # （1）准备一个停用词表，默认把停用词表中的词权重放低一点
    # （2）根据ltp的词性标注结果，按照词性赋值权重，这部分我已经实现了，参考get_weight()函数
    '''
    w_l1 = [0.5, 1.0, 1.0, 0.5]
    w_l2 = [0.5, 2.0, 1.0, 1.0, 0.5]
    w_l3 = [0.5, 1.0, 1.0, 0.5, 0.2]

    print('<', s1, ',', s2, '> sim:', end='')
    print(weighted_match_similarity(s1, s2, w1=w_l1, w2=w_l2))
    print('<', s1, ',', s3, '> sim:', end='')
    print(weighted_match_similarity(s1, s3, w1=w_l1, w2=w_l3))



