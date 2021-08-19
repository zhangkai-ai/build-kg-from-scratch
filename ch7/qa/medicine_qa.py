#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
医药图谱问答
"""
import re

# 医药图谱示例
medicine_kg = {
    "PD-1": {
        "antibody": "JS-001"
    },
    "Jie Fu": {
        "research": "PD-1"
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

    # 基于示例规则的语义解析、示例图谱的查询
    match = reg.match(text)
    if match:
        s = match.group("subject")
        p = match.group("predicate")
        # 图谱查询
        ans = medicine_kg.get(s)
        if ans:
            ans = ans.get(p)
        if ans:
            rst = {
                "service": "medicine_qa",
                "slot": {
                    "s": s,
                    "p": p,
                },
                "nlg": ans
            }
    return rst

