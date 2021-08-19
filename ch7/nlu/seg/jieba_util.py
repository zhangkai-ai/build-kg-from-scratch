#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
jieba分词
"""
import jieba
import jieba.posseg


class JiebaUtil:
    def __init__(self, user_dict=''):
        # 当用户自定义词表时，jieba会在系统词表基础上用user_dict进行更新操作
        if user_dict:
            # 词表格式：词条 频次
            # 通常频次可设置为3，但当jieba依旧无法分开的情况，需要调大频次的值
            jieba.load_userdict(user_dict)

    def jieba_cut(self, sentence, type=1):
        seg_list = []

        if type == 1:
            # 精确模式，默认
            seg_list = jieba.cut(sentence, cut_all=False)
        elif type == 2:
            # 全模式
            seg_list = jieba.cut(sentence, cut_all=True)
        elif type == 3:
            # 搜索引擎模式
            seg_list = jieba.cut_for_search(sentence)
        else:
            print("jieba input type error: parameter type out of range")

        return seg_list

    def jieba_postag(self, sentence):
        '''
        分词和词性标注
        :param sentence: 输入句子
        :return: 返回分词和词性标注的结果
        '''
        result = jieba.posseg.lcut(sentence)
        print(result)
        result = [w.word + '/' + w.flag for w in result]
        return result


jieba_util = JiebaUtil()  # user_dict='jieba_user_dict.txt')
# print(jieba_util.jieba_postag('晴天是周杰伦的歌吗？'))

