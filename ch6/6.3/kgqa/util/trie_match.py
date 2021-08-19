#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'winnie'

import os
import marisa_trie
import configparser
import json
from collections import defaultdict

__cf = configparser.ConfigParser()
__cf.read("./config.ini")
entity_tree_path = __cf.get("trie", "path") + 'entity.marisa'
property_tree_path = __cf.get("trie", "path") + 'property.marisa'

dict_path = os.getcwd().replace('test','')+ r"/data/dict/"
dict_name_list = ['book', 'body', 'blood_type', 'ethnic', 'country', 'occupation', 'country', 'city','constellation','position']


class RecordTrieTree(object):
    def __init__(self, persis_path=''):
        if persis_path:
            self.trie_tree = marisa_trie.Trie()
            self.trie_tree.load(persis_path)
        else:
            keys = []
            values = []
            dict_count = 0
            for dict_name in dict_name_list:
                with open(dict_path + dict_name + '.txt', 'r', encoding='utf8') as f:
                    raw_list = f.readlines()
                    for raw_line in raw_list:
                        raw_line = raw_line.strip()
                        keys.append(raw_line)
                        values.append(bytes([dict_count]))
                dict_count += 1
            self.trie_tree = marisa_trie.BytesTrie(zip(keys, values))

    def trie_match(self, sent):
        """
        Find all matches in the sent against the trie tree
        :param sent: The input unicode sentence string which is not segmented
        :return: {"key1":[u"match1", u"match2"], "key2":[u"match3", u"match4"], ...}
        """
        matched_dict = defaultdict(set)
        index = 0
        while index < len(sent):
            matched_list = self.trie_tree.prefixes(sent[index:])
            if matched_list:
                max_matched_word = ""
                for matched_word in matched_list:
                    if len(matched_word) >= len(max_matched_word):
                        max_matched_word = matched_word
                for matched_dict_index in self.trie_tree[max_matched_word]:
                    dict_id = int.from_bytes(matched_dict_index, "big")
                    matched_dict_name = dict_name_list[int(dict_id)]
                    matched_dict[matched_dict_name].add(max_matched_word)
                index += len(max_matched_word)
            else:
                index += 1
        matched_dict_list = {key:list(value) for key,value in matched_dict.items()}
        return matched_dict_list


class TrieTree(object):
    def __init__(self, persis_path=''):
        if persis_path:
            self.trie_tree = marisa_trie.Trie()
            self.trie_tree.load(persis_path)
        else:
            # 没有已有的trie树文件，构建一颗trie树
            keys = []
            with open('total_entity.txt', 'r', encoding='utf8') as f:
                for raw in f:
                    keys.append(raw.strip())
            # 构建trie树
            self.trie_tree = marisa_trie.Trie(keys)
            self.trie_tree.save('../data/trie.marisa')

    def trie_match(self, sent):
        """
        找出输入句中包含在trie树中的全部词条，并且支持最大匹配的存放，例如周杰伦，会返回周杰伦而非周杰
        :param sent: 输入的句子未分词
        :return: 匹配到的实体列表的list
        """
        matched_set = set()
        index = 0
        while index < len(sent):
            matched_list = self.trie_tree.prefixes(sent[index:])
            if matched_list:
                max_matched_word = ''
                # 存放最大的匹配结果
                for matched_word in matched_list:
                    if len(matched_word) >= len(max_matched_word):
                        max_matched_word = matched_word
                if max_matched_word:
                    matched_set.add(max_matched_word)
                    index += len(max_matched_word)
                else:
                    index += 1
            else:
                index += 1
        # 对匹配到的内容按照长度从大到小排序
        matched_list = sorted(list(matched_set), key=lambda m: len(m), reverse=True)
        return matched_list


trie_tree = RecordTrieTree()
entity_trie = TrieTree(entity_tree_path)
property_trie = TrieTree(property_tree_path)


if __name__ == "__main__":
    # trie_tree = TrieTree()#'../data/trie.marisa')
    print(trie_tree.trie_match('北京，中国，俄罗斯，鼻子，三体，巴基斯坦'))
    # sent = '牙床抠鼻子眼.net 软件工程师'
    # print(trie_tree.trie_match(sent))
    # ret = trie_tree.get_resolution_type()
    # print(ret[u'狗尾草'])
    # print(ret[u'狗尾草'][0])
    # print(ret[u'狗尾草'][1])
    # print(ret[u'狗尾草'][2])

    # sentence = u"你会不会你会你能你会不会怎么你喜不喜欢吗是谁啥怎么样是什么会讲吗会说吗怎样的关系关系如何好看吗狗尾草吗?"

    # matched_dict = trie_tree.trie_match(u"金牛座和白羊座很配啊")
    # matched_dict = entity_tree.trie_match(u"ch4")
    # print(repr(matched_dict).decode('unicode-escape'))
    # matched_dict = property_tree.trie_match(u"哪国人")
    # print(repr(matched_dict).decode('unicode-escape'))
    pass