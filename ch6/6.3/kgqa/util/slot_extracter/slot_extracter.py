#!/usr/bin/python
# coding:utf8

from util.slot_extracter.slot import Slot


class SlotExtracter(object):
    """
    slot extracter
    """
    slot_name = ''
    slot_value = ''
    slot = Slot("")

    def __init__(self):
        pass

    def extracter(self, *args):
        return self.slot

