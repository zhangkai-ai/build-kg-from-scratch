#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
通用图谱问答
"""
import re

# 百科图谱示例
common_kg = {
    "周杰伦": {
        "星座": "摩羯座"
    },
    "韩寒": {
        "星座": "天秤座"
    }
}

# 示例语义解析规则
reg = re.compile(u'(?P<subject>.+)(的)(?P<predicate>.+)(是|为|称|叫|在|属于|属)(?P<object>.+)')


def handler(user_id, nlu_dict, dst):
    """
    基于百科图谱的问答处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return:
    """
    text = nlu_dict["input"]
    rst = None
    s = None
    p = None
    ans = None

    # 多轮qa
    if dst:
        multi_turn_slot = nlu_dict["slot"]["multi_turn_slot"]
        # 图谱查询
        # 尝试替换subject
        s = multi_turn_slot
        ans = common_kg.get(s)
        if ans:
            p = dst["slot"]["p"]
            ans = ans.get(p)
        # 尝试替换predicate
        if not ans:
            s = dst["slot"]["s"]
            ans = common_kg.get(s)
            if ans:
                p = multi_turn_slot
                ans = ans.get(p)

    # 基于示例规则的语义解析、示例图谱的查询
    if not ans:
        match = reg.match(text)
        if match:
            s = match.group("subject")
            p = match.group("predicate")
            # 图谱查询
            ans = common_kg.get(s)
            if ans:
                ans = ans.get(p)
    # 组装返回结果
    if ans:
        rst = {
            "service": "common_qa",
            "slot": {
                "s": s,
                "p": p,
            },
            "nlg": ans
        }
    return rst

