#!/usr/bin/python
# -*-coding: utf-8 -*-

import sys
import re
import ch7.nlu.slot_extracter.reg_util  as reg_util
# reload(sys)
# sys.setdefaultencoding('utf-8')

zh_number = "零|一|二|三|四|五|六|七|八|九|十|百|千|万"
zh_number_dict = {"一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10","百":"100","千":"1000","万":"10000"}

def deal_height(sent):
    sent = sent.replace('吗','')
    pattern_0 = "(\\d|{zh_number})(尺|丈)".format(zh_number= zh_number)
    pattern_1 = "(\\d+|{zh_number})米((\\d+|{zh_number})+)".format(zh_number = zh_number)
    pattern_2 = "(\\d+)(厘米|公分|cm|CM)"
    pattern_3 = "((\\d+)|{zh_number}+)$".format(zh_number = zh_number)
    if re.search(pattern_3, sent):
        sent = sent + '厘米'

    regex_0 = re.search(pattern_0,sent)
    regex_1 = re.search(pattern_1, sent)
    regex_2 = re.search(pattern_2, sent)
    if regex_0:
        number = regex_0.group(1)
        if "尺" in sent:
            if number in zh_number_dict.keys():
                number = zh_number_dict[number]
                return str(int(number) * 33)
            else:
                return str(int(number) * 33)
        else:
            if number in zh_number_dict.keys():
                number = zh_number_dict[number]
                return str(int(number) * 333)
            else:
                return str(int(number) * 333)

    elif(regex_1):
        mi_q = regex_1.group(1)
        mi_h = regex_1.group(2)
        if mi_q in zh_number_dict.keys():
            mi_q = zh_number_dict[mi_q]
        if len(mi_h) == 1:
            if mi_h in zh_number_dict.keys():
                mi_h = zh_number_dict[mi_h]
            mi_h = mi_h + '0'
            return str(mi_q)+str(mi_h)
        else:
            string = "" + str(mi_q)
            for unit in mi_h:
                if unit in zh_number_dict.keys():
                    unit = zh_number_dict[unit]
                    string = string + str(unit)
                else:
                    string = string + str(unit)
            return string
    elif(regex_2):
        cm_q = regex_2.group(1)
        return cm_q

def deal_weight(sent):
    sent = sent.strip()
    pattern_1 = '((\\d|{zh_number})+)(千克|公斤|kg)'.format(zh_number=zh_number)
    pattern_2 = '((\\d|{zh_number})+)斤((\\d|{zh_number})+)?两?'.format(zh_number=zh_number)
    pattern_3 = '((\\d|{zh_number})+)$'.format(zh_number=zh_number)
    sent = sent.replace('吗',"")
    if re.search(pattern_3, sent):
        sent = sent + "斤"
    regex_1 = re.search(pattern_1, sent)
    regex_2 = re.search(pattern_2, sent)
    if regex_1:
        number_1 = regex_1.group(1)
        number_1 = reg_util.cn2dig(number_1)
        return str(int(number_1) * 2)
    elif(regex_2):
        number_1 = regex_2.group(1)
        number_1 = reg_util.cn2dig(number_1)
        number_2 = regex_2.group(3)
        if number_2:
            number_2 = reg_util.cn2dig(number_2)
            return str(number_1) + '.' + str(number_2)
        else:
            return str(number_1)

    else:
        return '0'
