#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
数据库信息同步
"""


def synchronize_from_db(db_name):
    """
    从数据库（如mysql）或者其他存储平台，拉取热点、用户画像、bot图谱等信息
    :param db_name: 对应的数据库名称
    :return: 数据库对应数据
    """
    data = {}
    if db_name == "hot_event":
        """
        some db query codes
        以下为返回示例
        """
        data = {
            "女篮": [
                ["女篮积极备战", 1565929940],
                ["女篮大胜波多黎各", 1566163045]
            ],
            "波多黎各": [
                ["女篮大胜波多黎各", 1566163045]
            ]
        }
    elif db_name == "user_related_entity":
        """
        some db query codes
        以下为返回示例
        """
        data = {
            "user_id": {
                "性别": "男",
                "运动": "健身房运动两天",
                "音乐": "七里香"
            }
        }
    elif db_name == "user_related_entity":
        """
        some db query codes
        以下为返回示例
        """
        data = {
            "bot_id": {
                "性别": "男",
                "名称": "Javis"
            }
        }
    return data
