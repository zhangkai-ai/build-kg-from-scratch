#!/usr/bin/python
# -*-coding: utf-8 -*-

from ch7.util.trie_match import TrieTree
from const import zh_number

desc_to_age_mapping = {
    "幼年": "0-7",
    "童年": "7-16",
    "少年": "7-16",
    "成年": "18-30",
    "青年": "18-30",
    "中年": "31-50",
    "老年": "60-100",
    "襁褓": "0",
    "孩提": "2-3",
    "髫年": "7",
    "黄口": "0-10",
    "舞勺之年": "13-15",
    "舞象之年": "15-20",
    "金钗之年": "12",
    "豆蔻年华": "13",
    "及笄之年": "15",
    "碧玉年华": "16",
    "桃李年华": "20",
    "梅之年": "24",
    "弱冠": "20",
    "而立": "30",
    "而立之年": "30",
    "不惑": "40",
    "不惑之年": "40",
    "半百": "50",
    "知命": "50",
    "花甲": "60",
    "耳顺": "60",
    "古稀": "70",
    "古稀之年": "70",
    "杖朝": "80",
    "杖朝之年": "80",
    "耄耋": "90",
    "耄耋之年": "90"
}

age_desc_trie_tree = TrieTree(list(desc_to_age_mapping))


def age_mapping(sent):
    sent = sent.replace('奔', '')
    age_string = ""
    for char_sent in sent:
        if char_sent in zh_number:
            later = str(int(zh_number[char_sent])-1)
            age_string = age_string + zh_number[char_sent]
            age_string = "{}0-{}0".format(later, age_string)
    return age_string


def age_extractor(sent):
    """
    两阶段匹配, 第一种是年龄指代直接对应数值, 第二种动态数值
    :param sent:
    :return:
    """
    slot_list = []
    matched_list = age_desc_trie_tree.trie_match(sent)
    for matched in matched_list:
        slot_list.append([matched, desc_to_age_mapping[matched]])
    return slot_list

rst = age_extractor("那还是我幼年的时候,直到我成年")
print(rst)
