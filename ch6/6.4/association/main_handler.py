#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
联想主入口
"""

import random
from loguru import logger
from data_access.association_generator import get_association_by_embedding, get_association_by_kg
from filter.hot_event_filter import filter_by_hot_event
from filter.user_profile_filter import filter_by_user_profile
from filter.bot_profile_filter import filter_by_bot_profile
from filter.context_filter import filter_by_context, update_context, check_context
from util.topic_classifier import classify_topic, main_part_extractor


def pipeline(sent, topic_set, user_id, bot_id='girl'):
    """
    联想模块pipeline
    :param sent: 待联想语句
    :param topic_set: 待联想话题列表
    :param user_id: 用户的id
    :param bot_id: bot的id
    :return:
    """
    # Step1: 产生候选话题集合，基于图谱的一跳关系，以及词向量扩展结果
    candidate_set = get_association_candidates(topic_set, sent)
    if not candidate_set:
        return {}
    logger.info('candidate generate num: {}'.format(len(candidate_set)))

    # Step2: 计算候选实体得分
    association_score_map = {}
    association_detail_map = {}
    for candidate in candidate_set:
        detail_dict = {}
        score = 0
        # 排序因素: 根据热点过滤
        hot_event_rst = filter_by_hot_event(candidate)
        if hot_event_rst:
            detail_dict["hot_event"] = hot_event_rst[0]
            score += hot_event_rst[1]
        # 排序因素: 与用户长期记忆的关联程度
        user_rst = filter_by_user_profile(user_id, candidate)
        if user_rst:
            detail_dict["user"] = user_rst[0]
            score += user_rst[1]
        # 排序因素: 与bot人设的关联程度
        bot_rst = filter_by_bot_profile(bot_id, candidate)
        if bot_rst:
            detail_dict["bot"] = bot_rst[0]
            score += bot_rst[1]
        # 排序因素: 与上下文的关联程度
        context_rst = filter_by_context(user_id, candidate)
        if context_rst:
            score += context_rst[1]

        association_score_map[candidate] = score
        association_detail_map[candidate] = detail_dict
    return association_score_map, association_detail_map


def get_association_candidates(topic_set, sent) -> set:
    """
    获取联想话题候选集合
    :param topic_set: 话题集合
    :param sent:
    :return:
    """
    candidate_set = set()
    for topic in topic_set:
        candidate_set.update(get_association_by_kg(topic, sent))
        candidate_set.update(get_association_by_embedding(topic))
    return candidate_set

connect_template = [
    '话说,',
    '说起来,',
    '想起来,'
]
hot_template = [
    '我最近看到消息说：',
    '我最近看到一个话题：',
    '最近大家好像在讨论：',
    '我最近看到一条新闻：',
    '我刚刚看到一条新闻说：',
    '最近我得知一条新闻：',
    '最近有一条新闻：',
    '最近有一条消息说：',
    '最近有一条话题：'
]


def generate_rely(topic, detail_dict) -> str:
    """
    生成联想回复
    :param topic: 话题
    :param detail_dict: 话题相关具体信息
    :return: 回复语句
    """
    reply_list = []
    if 'user' in detail_dict:
        detail = detail_dict['user']
        reply_list.append('没记错的话，{}是你的{}'.format(topic, detail))
    if 'bot' in detail_dict:
        detail = detail_dict['bot']
        reply_list.append('真巧，{}也是我的{}'.format(topic, detail))
    if 'hot_event' in detail_dict:
        detail = detail_dict['hot_event']
        reply_list.append(random.choice(connect_template) + random.choice(hot_template) + detail)
    reply = "。".join(reply_list)
    return reply


def extract_topics(sent) -> set:
    """
    话题抽取，可抽取的话题类型包括实体和概念
    :param sent: 输入语句
    :return: 话题集合
    """
    topic_set = set()
    # 方法1：基于文本分类，预设若干话题类别
    # topic_set.update(entity_linking(sent))
    topic_set.update(classify_topic(sent))
    # 方法2：基于主成分提取
    topic_set.update(main_part_extractor(sent))
    return topic_set


def handler(sent, user_id) -> dict:
    """
    联想模块主处理函数
    :param sent: 待联想语句
    :param user_id: 用户的id
    :return: 联想结果，联想到的话题和回复语句
    """
    topic_set = extract_topics(sent)
    if not topic_set:
        # 没有待联想话题，返回
        return {}
    # 检查上下文
    check_context(user_id)

    candidate_score_map, candidate_detail_map = pipeline(sent, topic_set, user_id)
    if not candidate_score_map:
        # 没有候选，继续
        return {}

    # 根据分数进行排序，选择得分最大的候选topic
    max_score = -1
    rst_topic = None
    for topic, score in candidate_score_map.items():
        if score > max_score:
            max_score = score
            rst_topic = topic
        elif score == max_score:
            # 如果分数相同，则50%概率替换当前候选，造成一定的随机性
            if random.random() < 0.5:
                rst_topic = topic
    if max_score == 0:
        # 没有合适的加权候选，随机返回
        rst_topic = random.choice(candidate_score_map.keys())

    rst_dict = {
        "topic": rst_topic,
        "reply": generate_rely(rst_topic, candidate_detail_map[rst_topic])
    }

    # 更新上下文
    update_context(user_id, rst_topic, sent)

    return rst_dict


if __name__ == "__main__":
    rst = handler('菩提本非树，明镜亦非台，本来无一物，何处染尘埃？', 'id_001', 3)
    print(rst)
