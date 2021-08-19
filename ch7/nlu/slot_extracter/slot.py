#!/usr/bin/python
# coding:utf8

import json


class Slot(object):
    slot_name = ''
    slot_type = ''
    slot_value = ''
    slot_default = ''

    def __init__(self, value, **kw):
        self.slot_value = value

    """
        保存额外的slot信息
    """
    def add_slot(self, name, value):
        self.__setattr__(name, value)

    """
        根据保存的slot key，获取其value
    """
    def get_slot_value(self, key):
        return getattr(self, key, None)

    def validate(self):
        pass

    """
       返回默认存储的value,如果有保存多个，可以用get_slot_value获取
    """
    @property
    def value(self):
        return self.slot_value

    def __str__(self):
        if isinstance(self.slot_value, dict):
            return json.dumps(self.slot_value)
        return self.slot_value

