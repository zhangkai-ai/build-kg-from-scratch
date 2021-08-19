#!/usr/bin/python
# -*-coding: utf-8 -*-

# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

zh_number = {u"一":"1",u"二":"2",u"三":"3",u"四":"4",u"五":"5",u"六":"6",u"七":"7",u"八":"8",u"九":"9",u"十":"10"}
age_type_1 = {u"幼年":"0-7",u"童年":"7-16",u"少年":"7-16",u"成年":"18-30",u"青年":"18-30",u"中年":"31-50",u"老年":"60-100"}
age_type_2 = {u"襁褓":"0",u"孩提":"2-3",u"髫年":"7",u"黄口":"0-10",u"舞勺之年":"13-15",u"舞象之年":"15-20",u"金钗之年":"12",
              u"豆蔻年华":"13",u"及笄之年":"15",u"碧玉年华":"16",u"桃李年华":"20",u"梅之年":"24",u"弱冠":"20",u"而立":"30",
              u"而立之年":"30",u"不惑":"40",u"不惑之年":"40",u"半百":"50",u"知命":"50",u"花甲":"60",u"耳顺":"60",u"古稀":"70",
              u"古稀之年":"70",u"杖朝":"80",u"杖朝之年":"80",u"耄耋":"90",u"耄耋之年":"90"}

def age_type_3(sent):
    sent = sent.replace('奔','')
    age_string = ""
    for char_sent in sent:
        if char_sent in zh_number:
            later = str(int(zh_number[char_sent])-1)
            age_string = age_string + zh_number[char_sent]
    age_string = later + '0'+'-'+age_string + '0'
    return age_string