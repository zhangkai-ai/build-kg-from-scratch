#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
bot图谱问答
"""
import re

# bot人设图谱示例
bot_kg = {
    "男性": {
        "星座": "金牛座"
    },
    "女性": {
        "星座": "白羊座"
    }
}
bot_id = "男性"

# 示例语义解析规则
reg = re.compile(u'(你)(的)(?P<predicate>.+)(是|为|称|叫|在|属于|属)(?P<object>.+)')


def handler(user_id, nlu_dict, dst):
    """
    基于bot人设图谱的问答处理函数
    :param user_id: 用户id
    :param nlu_dict: nlu执行结果字典
    :param dst: 历史对话状态结果
    :return:
    """
    text = nlu_dict["input"]
    rst = None
    p = None
    ans = None

    # 多轮qa
    if dst:
        multi_turn_slot = nlu_dict["slot"]["multi_turn_slot"]
        # 图谱查询
        # 尝试替换subject
        # TODO: 扩增对bot的指代
        if multi_turn_slot in ["你"]:
            ans = bot_kg.get(bot_id)
            if ans:
                p = dst["slot"]["p"]
                ans = ans.get(p)
        # 尝试替换predicate
        if not ans:
            ans = bot_kg.get(bot_id)
            if ans:
                p = dst["slot"][multi_turn_slot]
                ans = ans.get(p)

    # 基于示例规则的语义解析、示例图谱的查询
    if not ans:
        match = reg.match(text)
        if match:
            p = match.group("predicate")
            # 图谱查询
            ans = bot_kg.get(bot_id)
            if ans:
                ans = ans.get(p)
    # 组装返回结果
    if ans:
        rst = {
            "service": "bot_qa",
            "slot": {
                "s": "bot",
                "p": p,
            },
            "nlg": ans
        }
    return rst

