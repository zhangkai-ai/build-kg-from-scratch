#!/usr/bin/python
# coding:utf8

from util.slot_extracter.slot import Slot


class TimeSlot(Slot):

    def __init__(self, value, **kw):
        self.slot_value = value

    def validate(self):
        pass

