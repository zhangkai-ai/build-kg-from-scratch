#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
状态机管理
"""
import time

dst_dict = {}
'''
dst_dict = {
    "user_id_1": [dst_1, dst2]
}
'''


def get_dst(user_id):
    """
    获取状态机中的dst信息，每个user对应维护一个状态机
    :param user_id: 用户id
    :return:
    """
    valid_dst_list = []
    dst_list = dst_dict.get(user_id, None)
    if dst_list:
        now_time = time.time()
        # 多轮窗口，轮数限制
        if len(dst_list) > 5:
            dst_list.pop(0)
        for dst in dst_list:
            dst_time = dst.get('time', 0)
            # 多轮时间窗口，单位s，由远及近加入
            if now_time - dst_time <= 600:
                valid_dst_list.append(dst)
    valid_dst_list.reverse()
    return valid_dst_list


def add_dst(user_id, dst):
    """
    添加新的dst信息（本轮对话结果）到状态机中
    :param user_id: 用户id
    :param dst: 对话状态追踪信息
    :return:
    """
    dst_list = dst_dict.get(user_id, None)
    if dst_list:
        dst_list.append(dst)
    else:
        dst_dict[user_id] = [dst]

