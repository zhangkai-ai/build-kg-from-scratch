#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
热点过滤
"""
import time
from data_access.db_synchronizer import synchronize_from_db


topic_event_mapping = {}


def update_hot_event():
    """
    从数据库同步本地热点事件
    :return: None
    """
    topic_event_mapping.clear()
    update_rst = synchronize_from_db("hot_event")
    topic_event_mapping.update(update_rst)
update_hot_event()


def filter_by_hot_event(topic):
    """
    过滤功能函数
    :param topic: 候选话题
    :return: 相关热点信息和话题得分
    """
    event_list = topic_event_mapping.get(topic, None)
    if event_list:
        event_detail = ''
        max_score = 0
        for event_info in event_list:
            time_interval = time.time() - event_info[1]
            if time_interval < 3600*24*2:
                score = 1
            elif time_interval < 3600*24*4:
                score = 0.6
            elif time_interval < 3600*24*5:
                score = 0.4
            else:
                score = 0.2
            if score >= max_score:
                max_score = score
                event_detail = event_info[0]
        return [event_detail, max_score]
