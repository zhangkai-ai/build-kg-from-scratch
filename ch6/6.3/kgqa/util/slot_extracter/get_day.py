#!/usr/bin/python
# -*-coding: utf-8 -*-


import datetime
import re
import calendar
# from util.logger import logger
from util.slot_extracter.slot_extracter import SlotExtracter
from util.slot_extracter.time_slot import TimeSlot
import time

# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')


class TimeSlotExtracter(SlotExtracter):
    """Extracting time information.

    Extracting time period, time point, and time frequency!
    Attributes:
        tpd: time period
        tpt: time point
        tfy: time frequency
    """

    def __init__(self):
        self.time_unit = "年|月|周|礼拜|星期|天|日|时|小时|钟头|分|分钟"
        self.time_limit_word = "今|明|本|下|下下|上|上上|这|昨|前|后|大前|大后|来|去|未来"
        self.number_word = "[0-9一二两三四五六七八九十零半日天末]"
        self.frequency_word = "每[间相]?[隔过个]?"
        self.char2num = {"一": "1",
                         "二": "2",
                         "三": "3",
                         "四": "4",
                         "五": "5",
                         "六": "6",
                         "七": "7",
                         "八": "8",
                         "九": "9",
                         "十": "0",
                         "零": "0",
                         "日": "7",
                         "天": "7",
                         "末": "7",
                         "两": "2"
                         }

    def get_num_from_char(self, char_num):
        """
        Replace "一零二" with 102

        :param char_num:
        :return:
        """
        char_num_copy = char_num
        for word in char_num:
            if word == "十":
                if len(char_num_copy) == 1:
                    char_num_copy = char_num_copy.replace(word, "10")

                elif len(char_num_copy) > 1 and char_num_copy.index(u'十') == 0:
                    char_num_copy = char_num_copy.replace(u'十', u'1')
                elif len(char_num_copy) > 1 and char_num_copy.index(u'十') < len(char_num) - 1:
                    char_num_copy = char_num_copy.replace(u'十', u'')
                elif len(char_num_copy) > 1 and char_num_copy.index(u'十') == len(char_num_copy) - 1:
                    char_num_copy = char_num_copy.replace(u'十', u'0')
            else:
                if word in self.char2num:
                    char_num_copy = char_num_copy.replace(word, self.char2num[word])
        return char_num_copy

    @staticmethod
    def get_num_from_time_unit(limit_word):
        """
        Converting limiting word to int!

        :param limit_word:
        :return:
        """
        add_num = 0
        if limit_word in ["今", "本", "这"]:
            add_num = 0
        elif limit_word in ["明", "下", "来"]:
            add_num = 1
        elif limit_word in ["上", "昨", "去"]:
            add_num = -1
        elif limit_word in ["前", "上上"]:
            add_num = -2
        elif limit_word in ["后", "下下"]:
            add_num = 2
        elif limit_word in ["大前"]:
            add_num = -3
        elif limit_word in ["大后"]:
            add_num = 3
        return add_num

    def parsing_hour_min(self, result_hour, result_min, result_limit):
        """
        Parsing hour,min to num!

        :param result_hour: hour by regular matcher
        :param result_min: min by regular matcher
        :param result_limit: time_limit by regular matcher
        :return:
        """
        result_hour = self.get_num_from_char(result_hour)
        result_hour = int(result_hour)
        if result_hour > 23:
            result_hour = 0
        if result_limit in ["下午", "晚饭时间", "黄昏", "晚上", "晚", "午夜", "夜间", "夜里", "黑夜"] \
                and result_hour < 12:
            result_hour = result_hour + 12
        else:
            result_hour = result_hour
        if result_min:
            result_min1 = self.get_num_from_char(result_min)
            result_min1 = result_min1.replace("分", "").replace("半", "30").replace(u'刻', u'')
            if u'刻' in result_min:
                result_min = int(result_min1) * 15
            else:
                result_min = int(result_min1)
        else:
            result_min = 0
        if result_hour > 23:
            result_hour = result_hour - 12
        return result_hour, result_min

    def get_day(self, text):
        """
        Extracting time point!
        :param text:
        :return:
        """
        # print('非当天时间点')
        now_time = datetime.datetime.now()

        global max_tpt
        max_tpt = 0
        regex_1 = "过([去了])?({number_word}+)([个整])?(日|天|周|礼拜|星期|月|年)". \
            format(number_word=self.number_word)
        regex_2 = "[再还]([剩有过])([下了])?({number_word}+)([个整])?(日|天|周|礼拜|星期|月|年)". \
            format(number_word=self.number_word)
        # regex_3 = "((?:(%s+)|(%s))年)?(%s+月)?(%s+)(日|号|天)?([后前])?" \
        #           % (self.number_word, self.time_limit_word, self.number_word, self.number_word)
        regex_3 = "({number_word}+年)?((({number_word}+月)({number_word}+(日|号|天)*)?)|({number_word}+(日|号|天)+))({time_limit_word})?". \
            format(number_word=self.number_word, time_limit_word=self.time_limit_word)
        regex_4 = "({time_limit_word})个?(星期|礼拜|周)?的?(周|礼拜|星期)({number_word}+)". \
            format(time_limit_word=self.time_limit_word, number_word=self.number_word)
        regex_5 = "({time_limit_word})(个)?(日|天|早|晚|夜)". \
            format(time_limit_word=self.time_limit_word)
        regex_6 = "({number_word})月份".format(number_word=self.number_word)
        #过了一个月
        pattern_1 = re.compile(regex_1).search(text)

		
        #再过一周
        pattern_2 = re.compile(regex_2).search(text)
        
        #11月11号
        pattern_3 = re.compile(regex_3).search(text)
        
        #下星期的星期二
        pattern_4 = re.compile(regex_4).search(text)
        
        pattern_5 = re.compile(regex_5).search(text)

        pattern_6 = re.compile(regex_6).search(text)

        lp_1 = len(pattern_1.group(0)) if pattern_1 else 0
        lp_2 = len(pattern_2.group(0)) if pattern_2 else 0
        lp_3 = len(pattern_3.group(0)) if pattern_3 else 0
        lp_4 = len(pattern_4.group(0)) if pattern_4 else 0
        lp_5 = len(pattern_5.group(0)) if pattern_5 else 0
        lp_6 = len(pattern_6.group(0)) if pattern_6 else 0


        dict_p = {pattern_1: lp_1, pattern_2: lp_2, pattern_3: lp_3, pattern_4: lp_4, pattern_5: lp_5, pattern_6: lp_6}
        len_pattern = sorted(dict_p, key=lambda x: dict_p[x])[-1]  #对于冲突的正则规则，采用匹配的最大长度为最终的匹配 例如：过一周 和 再过一周----> 选择再过一周
        if len_pattern is None:
            max_tpt = 0
            return {"tpt": "",
                    "tpt_normal": ""}

        if pattern_1 == len_pattern:
            num1 = pattern_1.group(2)
            unit1 = pattern_1.group(4)
            now_time = datetime.datetime.now()
            num1 = self.get_num_from_char(num1) #中文数字转阿拉伯
            num1 = int(num1)
            max_tpt = len(pattern_1.group(0))
            if unit1 in ["日", "天", "月", "年", "星期", "周", "礼拜"]:
                if unit1 in ["星期", "周", "礼拜"]:
                    num = num1 * 7
                    data1 = now_time.date() - datetime.timedelta(days=num)
                if unit1 in ["日", "天"]:
                    num = num1 * 1
                    data1 = now_time.date() - datetime.timedelta(days=num)
                if unit1 in ["年"]:
                    num = num1 * 365
                    data1 = now_time.date() - datetime.timedelta(days=num)
                if unit1 in ["月"]:
                    num1 = calendar.monthrange(now_time.year, now_time.month - num1)[1]
                    # num = num1 * 30
                    data1 = now_time.date() - datetime.timedelta(days=num1)
            time_str = pattern_1.group()
            return {"tpt": time_str.encode('utf-8'),
                    "tpt_normal": data1.strftime("%m/%d"),
                    }

        elif pattern_2 == len_pattern:
            num2 = pattern_2.group(3)
            unit2 = pattern_2.group(5)
            now_time = datetime.datetime.now()
            num2 = self.get_num_from_char(num2)
            num2 = int(num2)
            max_tpt = len(pattern_2.group(0))
            if unit2 in ["日", "天", "月", "年", "星期", "周", "礼拜"]:
                if unit2 in ["星期", "周", "礼拜"]:
                    num = num2 * 7
                    data2 = now_time.date() + datetime.timedelta(days=num)
                if unit2 in ["日", "天"]:
                    num = num2 * 1
                    data2 = now_time.date() + datetime.timedelta(days=num)
                if unit2 in ["年"]:
                    num = num2 * 365
                    data2 = now_time.date() + datetime.timedelta(days=num)
                if unit2 in ["月"]:
                    num2 = calendar.monthrange(now_time.year, now_time.month)[1]
                    # num = num2 * 30
                    data2 = now_time.date() + datetime.timedelta(days=num2)
            time_str = pattern_2.group()
            return {"tpt": time_str.encode('utf-8'),
                    "tpt_normal": data2.strftime("%m/%d"),
                    }

        if pattern_3 == len_pattern:
            year_word = pattern_3.group(1)
            month_word = pattern_3.group(4)
            day_word_1 = pattern_3.group(5)
            day_word_2 = pattern_3.group(7)
            time_limit = pattern_3.group(9)
            max_tpt = len(pattern_3.group(0))
            s = "日|天|号"

            # year
            if year_word:
                year = year_word.replace("年", "")
                if year in self.time_limit_word:
                    add_num = self.get_num_from_time_unit(year)
                    year = now_time.year + add_num
                else:
                    year = self.get_num_from_char(year)
                    if len(year) == 2:
                        year = int(str(now_time.year)[0:2] + year)
                        if year > now_time.year:
                            year = year - 100
                    else:
                        year = int(year)
                        if year > 9999:
                            year = 9999
            else:
                year = now_time.year
            # month
            day_word = 0
            if month_word:
                if day_word_1:
                    day_word_1 = re.sub(s, "", day_word_1)
                    day_word = self.get_num_from_char(day_word_1)
                month_word = month_word.replace("月", "")
                month_word = self.get_num_from_char(month_word)
                month = int(month_word)
            else:
                month = now_time.month
                if day_word_2:
                    day_word_2 = re.sub(s, "", day_word_2)
                    day_word = self.get_num_from_char(day_word_2)
            day = int(day_word)
            if month > 12 or month == 0:
                logger.info("month is wrong: %s" % str(month))
                month = 12 if month > 12 else 1
            # day
            if day == 0 or day > calendar.monthrange(year, month)[1]:
                logger.info("day is wrong: %s" % str(day))
                day = calendar.monthrange(year, month)[1] if day > calendar.monthrange(year, month)[1] else 1
            if time_limit in [u'前', u'后']:
                if time_limit == u'后':
                    normal_date = datetime.datetime.now() + datetime.timedelta(days=day)
                if time_limit == u'前':
                    normal_date = datetime.datetime.now() + datetime.timedelta(days=day * (-1))
            else:
                normal_date = datetime.datetime(year, month, day).date()
            time_str = pattern_3.group()
            return {"tpt": time_str.encode('utf-8'),
                    "tpt_normal": normal_date.strftime("%m/%d"),
                    }
        elif (pattern_4 or pattern_5) == len_pattern:
            pattern_45 = pattern_4 if pattern_4 else pattern_5
            limit_word = pattern_45.group(1)
            unit_word = pattern_45.group(3)
            max_tpt = len(pattern_45.group(0))

            else_word = ''
            try:
                num_word = pattern_45.group(4)
                temp_word = num_word
                if len(num_word) > 1:
                    num_word = num_word[0]
                    else_word = temp_word[1:]
                num_word = self.get_num_from_char(num_word)
            except:
                num_word = None
            add_num = 0
            num = None
            base_date = now_time
            if limit_word:
                add_num = self.get_num_from_time_unit(limit_word)
            if unit_word:
                if unit_word in ["星期", "周", "礼拜"]:
                    weekday = now_time.isoweekday()
                    base_date = now_time - datetime.timedelta(days=weekday)
                    add_num = add_num * 7
                elif unit_word in ["日", "天", "早", "晚", "夜"]:
                    base_date = now_time
                    add_num = add_num * 1
            if num_word:
                num = self.char2num.get(num_word, num_word)
                try:
                    num = int(num)
                    if num > 7:
                        num = num / 10
                except Exception as e:
                    logger.error(e)
                    logger.info("error: 时间点中的数字转换出问题")
                    num = None
            if num:
                base_date = base_date + datetime.timedelta(days=num)
            normal_date = base_date + datetime.timedelta(days=add_num)
            if else_word:
                a = pattern_45.group().replace(else_word, '')
            else:
                a = pattern_45.group()
            time_str = re.split("{number_word}".format(number_word=self.number_word), pattern_45.group())
            time_str = a[a.index(time_str[0][-1]):a.index(time_str[0][-1]) + 2]
            # modify by xiliu
            for x in ["早", "晚", "夜"]:
                time_str = time_str.replace(x, "")
            return {"tpt": time_str.encode('utf-8'),
                    "tpt_normal": normal_date.strftime("%m/%d"),
                    }

        elif (pattern_6) == len_pattern:
            max_tpt = len(pattern_6.group(0))
            month_number = pattern_6.group(1)
            num1 = self.get_num_from_char(month_number)
            num1 = int(num1)
            if num1<10:
                time_str = '0'+str(num1) + '/01-'+'0'+str(num1)+'/'+str(calendar.mdays[num1])
            else:
                time_str = str(num1) + '/01-' + str(num1) + '/' + str(calendar.mdays[num1])
            return {"tpt": month_number + "月份",
                    "tpt_normal": time_str}

        else:
            max_tpt = 0
            return {"tpt": "",
                    "tpt_normal": ""}

    def get_day_period(self, text):
        global max_tpd
        max_tpd = 0
        now_time = datetime.datetime.now()
        regex_1 = "([刚刚][过|走|完|结束])"
        regex_2 = "([马上|立马|就]要?[来到])"
        regex_3 = "({time_limit_word})个?(月|周|礼拜|星期)". \
            format(time_limit_word=self.time_limit_word)

        pattern_1 = re.compile(regex_1).search(text)
        pattern_2 = re.compile(regex_2).search(text)
        pattern_3 = re.compile(regex_3).search(text)
        if pattern_1:
            start_date = now_time.date() - datetime.timedelta(days=7)
            end_date = now_time.date() - datetime.timedelta(days=1)
            day_str = pattern_1.group()
            max_tpd = len(pattern_1.group(0))
            return {"tpt": day_str.encode('utf-8'),
                    "tpt_normal": start_date.strftime("%m/%d") + "-" + end_date.strftime("%m/%d")
                    }
        elif pattern_2:
            start_date = now_time.date() + datetime.timedelta(days=1)
            end_date = now_time.date() + datetime.timedelta(days=7)
            day_str = pattern_2.group()
            max_tpd = len(pattern_2.group(0))
            return {"tpt": day_str.encode('utf-8'),
                    "tpt_normal": start_date.strftime("%m/%d") + "-" + end_date.strftime("%m/%d")
                    }
        elif pattern_3:
            limit_word = pattern_3.group(1)
            tpd_word = pattern_3.group(2)
            add_num = 0
            max_tpd = len(pattern_3.group(0))
            if limit_word:
                add_num = self.get_num_from_time_unit(limit_word)
            if tpd_word:
                if tpd_word in ["星期", "周", "礼拜"]:
                    weekday = datetime.datetime.now().isoweekday()
                    start_date = now_time - datetime.timedelta(days=weekday - 1)
                    end_date = start_date + datetime.timedelta(days=6)
                    add_num = add_num * 7
                    start_date = start_date + datetime.timedelta(days=add_num)
                    end_date = end_date + datetime.timedelta(days=add_num)
                elif tpd_word in ["月"]:
                    last_day = calendar.monthrange(now_time.year, now_time.month + add_num)[1]
                    start_day = 1
                    start_date = datetime.date(now_time.year, now_time.month + add_num, start_day)
                    end_date = datetime.date(now_time.year, now_time.month + add_num, last_day)
            time_str = pattern_3.group()
            return {"tpt": time_str.encode('utf-8'),
                    "tpt_normal": start_date.strftime("%m/%d") + "-" + end_date.strftime("%m/%d")}

        else:
            return {"tpt": "",
                    "tpt_normal": ""}

    def extracter(self, text):
        get_day = self.get_day(text)
        get_day_period = self.get_day_period(text)
        # print get_day,1,get_day_period,2
        if max_tpt >= max_tpd and max_tpt > 0:
            return TimeSlot({"tpt": get_day,
                    "tfy": "",
                    "uc": "",
                    "tpd": ""})
        elif max_tpd > max_tpt and max_tpd > 0:
            return TimeSlot({"tpt": get_day_period,
                    "tfy": "",
                    "uc": "",
                    "tpd": ""})
        else:
            # logger.info("Get Birthday Date Error:" + str(Exception))
            return TimeSlot({"tpt": "",
                    "tfy": "",
                    "uc": "",
                    "tpd": ""})


time_extractor = TimeSlotExtracter()

if __name__ == "__main__":
    # text_list = [
    #     "我的生日刚过", "老娘出生那天是11月11号",
    #     "我的生日在农历十月十九号", "我的生日在今天",
    #     "我的生日是昨天", "今天是我的生日",
    #     "我下个月过生日", "我的生日过了一个月了",
    #     "23号我过生日快乐", "我的生日是31号",
    #     "我的生日过了一个月了", "我的生日还有一个星期",
    #     "我的生日在下下个星期三", "我的生日在下下周",
    #     "我的生日刚过3天", "我的生日刚刚过", "我的生",
    #     "我的生日过了一个月了", "我的生日是下个星期",
    #     "我的生日马上到了", "再过一周就是我生日了",
    #     "生日是下个星期的星期一", u'下礼拜星期二是我生日',
    #     u'下个星期的星期二是我生日', u'再过一周就是我生日了']
    text_list = [
    #  "下星期的星期二",
        "一九九八年1月18号",
    #   "我的生日还有一个月",
    #    u'下个星期的星期二是我生日',
    #   u'再过一周就是我生日了',
    #   u'我的生日还有一个星期'
    #    "我的生日是下下周",
    ]
    for text in text_list:
        time_module = TimeSlotExtracter()
        result = time_module.extracter(text)
        print(result)
