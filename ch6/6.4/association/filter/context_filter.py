#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
对话上下文过滤
"""
import time

time_window = 3600*10
user_context_topic_dict = {}


def check_context(user_id):
    """
    句子输入后，直接执行该函数，根据时间和轮数对context进行更新
    :param user_id: 用户id
    :return: None
    """
    now_time = time.time()
    if user_id in user_context_topic_dict:
        context_topic_dict = user_context_topic_dict[user_id]
        for topic in context_topic_dict:
            update_time = context_topic_dict[topic][0]
            turn_past = context_topic_dict[topic][1]
            sent_past = context_topic_dict[topic][2]
            if now_time - update_time > time_window:
                context_topic_dict.pop(topic)
            else:
                context_topic_dict[topic] = [update_time, turn_past+1, sent_past]


def update_context(user_id, topic, sent):
    """
    模块结束时更新context，将本轮出现的实体加入到context
    :param user_id: 用户id
    :param topic: 结果话题
    :param sent: 输入语句
    :return: None
    """
    now_time = time.time()
    if user_id in user_context_topic_dict:
        context_entity_dict = user_context_topic_dict[user_id]
        context_entity_dict[topic] = [now_time, 0, sent]
    else:
        user_context_topic_dict[user_id] = {topic: [now_time, 0, sent]}


def filter_by_context(user_id, topic):
    """
    过滤功能函数
    :param user_id: 用户id
    :param topic: 候选话题
    :return: 匹配得分和匹配依据(即涉及实体所在的上下文句子)
    """
    context_entity_dict = user_context_topic_dict.get(user_id, {})
    data_tuple = context_entity_dict.get(topic, None)
    if data_tuple:
        turn_past = data_tuple[1]
        sent = data_tuple[2]
        score = 1 - (turn_past * 1.0 - 1) / 10
        if score < 0:
            score = 0
        return [sent, score]
