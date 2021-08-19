#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
用户画像过滤
"""
from data_access.db_synchronizer import synchronize_from_db


user_related_topic_dict = {}


def update_user_related_entity():
    """
    从数据库同步用户画像信息
    :return: None
    """
    update_rst = synchronize_from_db("user_related_entity")
    user_related_topic_dict.update(update_rst)
update_user_related_entity()


def filter_by_user_profile(user_id, topic):
    """
    过滤功能函数
    :param user_id: 用户id
    :param topic: 候选话题
    :return: 相关用户信息和话题得分
    """
    related_topic_dict = user_related_topic_dict.get(user_id, None)
    topic_detail = related_topic_dict.get(topic, None)
    return [topic_detail, 1]
