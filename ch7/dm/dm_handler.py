#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
对话管理
"""
import re
from loguru import logger
from qa import bot_qa, common_qa, medicine_qa, user_qa, ir_qa, mr_qa
from chat import hello_chat, association_chat
from dm.dst_manager import get_dst
from util.multi_thread_util import thread_factory


def dm_main_handler(user_id, nlu_dict):
    """
    对话管理主处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :return: 本轮对话执行结果
    """
    # 候选服务列表
    candidate_service_list = []

    # 从dst中获取前几轮的候选结果
    dst_list = get_dst(user_id)
    logger.info("DST Candidate: {}".format(str(dst_list)))

    dst = multi_turn_policy(nlu_dict, dst_list)
    logger.info("DST: {}".format(str(dst_list)))

    # 加入多轮意图
    if dst and dst["service"] == "qa":
        candidate_service_list.extend(["bot_qa", "common_qa", "medicine_qa", "user_qa"])

    # 处理正常意图，添加至候选服务列表，不同意图，候选意图的选择策略也不同
    intent = nlu_dict['intent']
    if intent == 'hello':
        # 打招呼意图，不进行任何其他服务调用
        candidate_service_list.append("hello_chat")
    elif intent == 'qa':
        # qa粗意图，遍历所有四个QA服务，ir和mr作为补充
        if not dst:
            candidate_service_list.extend(["bot_qa", "common_qa", "medicine_qa", "user_qa"])
        candidate_service_list.extend(["ir_qa", "mr_qa"])
    elif 'qa' in intent:
        # qa细意图，仅执行细意图对应的服务，ir和mr作为补充
        candidate_service_list.append(intent)
        candidate_service_list.extend(["ir_qa", "mr_qa"])
    elif intent == 'chat':
        # 闲聊意图，执行联想服务
        candidate_service_list.append("association_chat")
    logger.info("Candidate Services: {}".format(str(candidate_service_list)))

    # 执行候选服务
    rst_list = service_excute(candidate_service_list, user_id, nlu_dict, dst)
    logger.info("Candidate RST: {}".format(str(rst_list)))
    rst = service_rank(rst_list)
    logger.info("Service RST: {}".format(str(rst)))

    return rst


reg_multi_turn_qa = re.compile("(那么|那)?(.+?)(的)?(怎么样|好吗|怎样|如何|呢)")


def multi_turn_policy(nlu_dict, dst_list):
    """
    多轮策略选择器
    :param nlu_dict: nlu执行结果字典
    :param dst_list: dst候选列表
    :return:
    """
    dst = None
    text = nlu_dict["input"]

    match = reg_multi_turn_qa.search(text)
    if match and dst_list:
        multi_turn_slot = match.group(2)
        for candidate in dst_list:
            service = candidate["service"]
            # 只对qa进行多轮处理
            # 同一个dst意图，只取时间最近的一个
            if "qa" in service:
                dst = candidate
                dst["service"] = "qa"
                nlu_dict["slot"]["multi_turn_slot"] = multi_turn_slot
                break
    return dst


def service_excute(service_list, user_id, nlu_dict, dst):
    """
    服务执行器，并行化执行任务列表service_list，同步完成后，将服务结果打包返回
    :param service_list: 待执行的服务列表
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return: 任务列表对应的执行结果
    """
    thread_task_list = []
    # 添加并行任务
    for service_name in service_list:
        # 当意图名称与服务名称一致时，用eval方式执行对应服务也可以
        # eval("thread_task_list.append(thread_factory.add_thread({}.handler, *(user_id, nlu_dict, dst)))".format(
        #     service_name))
        if service_name == "hello_chat":
            thread_task_list.append(thread_factory.add_thread(hello_chat.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "bot_qa":
            thread_task_list.append(thread_factory.add_thread(bot_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "common_qa":
            thread_task_list.append(thread_factory.add_thread(common_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "medicine_qa":
            thread_task_list.append(thread_factory.add_thread(medicine_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "user_qa":
            thread_task_list.append(thread_factory.add_thread(user_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "ir_qa":
            thread_task_list.append(thread_factory.add_thread(ir_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "mr_qa":
            thread_task_list.append(thread_factory.add_thread(mr_qa.handler, *(user_id, nlu_dict, dst)))
        elif service_name == "association_chat":
            thread_task_list.append(thread_factory.add_thread(association_chat.handler, *(user_id, nlu_dict, dst)))
    # 获取并行任务的执行结果
    rst_list = []
    for thread_task in thread_task_list:
        rst = thread_factory.get_rst(thread_task)
        rst_list.append(rst)
    return rst_list


def service_rank(candidate_list):
    """
    服务执行结果排序，优先选择candidate_list非空的第一个执行结果
    :param candidate_list:
    :return:
    """
    rst = None
    for candidate in candidate_list:
        if candidate:
            rst = candidate
            break
    return rst

