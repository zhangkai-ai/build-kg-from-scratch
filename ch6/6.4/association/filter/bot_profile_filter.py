#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
bot图谱过滤
"""
from data_access.db_synchronizer import synchronize_from_db


bot_related_topic_dict = {}


def update_bot_related_entity():
    """
    从数据库同步bot图谱信息
    :return: None
    """
    update_rst = synchronize_from_db('bot_related_entity')
    bot_related_topic_dict.update(update_rst)
update_bot_related_entity()


def filter_by_bot_profile(bot_id, topic):
    """
    过滤功能函数
    :param bot_id: bot的id
    :param topic: 候选话题
    :return: 相关bot信息和得分
    """
    related_topic_dict = bot_related_topic_dict.get(bot_id, {})
    topic_detail = related_topic_dict.get(topic, None)
    return [topic_detail, 1]
