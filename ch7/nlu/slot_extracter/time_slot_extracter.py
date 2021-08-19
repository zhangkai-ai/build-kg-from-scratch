#!/usr/bin/python
# -*-coding: utf-8 -*-

import datetime
import re
import calendar
from time_slot import TimeSlot
from slot_extracter import SlotExtracter


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
        self.time_limit_word = "今|明|本|下|上|这|昨|前|后|大前|大后|来|去|未来"
        self.number_word = "[0-9一二两三四五六七八九十零半天末]"
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
        self.time_intra_day = {
            "早饭时间": "早[饭餐]的?时[候间]",
            "早茶时间": "早茶的?时[候间]",
            "早上": "早上|早|早晨",
            "上午": "上午",
            "午休": "午休|中午休息的?时[候间]",
            "中午": "中午",
            "午饭时间": "午[饭餐]的?时[候间]",
            "午茶": "午茶的?时[候间]",
            "下午": "下午",
            "晚饭时间": "晚[饭餐]的?时[候间]",
            "黄昏": "黄昏",
            "晚上": "晚上|晚|夜间|夜里|黑夜",
            "午夜": "午夜",
            "凌晨": "凌晨",
            "白天": "白天"
        }
        self.time_intra = "早[饭餐]的?时[候间]|早茶的?时[候间]|早上|早|早晨|上午|中午休息的?时[候间]|中午|午[饭餐]的?时[候间]|" \
                          "午休|午茶的?时[候间]|下午|晚[饭餐]的?时[候间]|黄昏|晚上|晚|夜间|夜里|黑夜|午夜|凌晨|白天"
        self.time_intra_day_range = {
            "早上": [7, 9],
            "早饭时间": [7, 8],
            "早茶时间": [10, 11],
            "上午": [8, 12],
            "中午": [12, 14],
            "午饭时间": [12, 13],
            "午休": [13, 14],
            "午茶": [15, 16],
            "下午": [14, 18],
            "晚饭时间": [18, 20],
            "黄昏": [18, 19],
            "晚上": [19, 6],
            "午夜": [0, 2],
            "凌晨": [0, 6],
            "白天": [6, 19]
        }
        self.reg_uncertain_time = re.compile("平时|最近|刚刚|刚才|刚|曾经|以前|一会儿?|接下来|接着|下次|等下|马上|立马|等会|当前|现在|实时|一直")

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

                elif len(char_num_copy) > 1 and char_num_copy.index('十') == 0:
                    char_num_copy = char_num_copy.replace('十', '1')
                elif len(char_num_copy) > 1 and char_num_copy.index('十') < len(char_num)-1:
                    char_num_copy = char_num_copy.replace('十', '')
                elif len(char_num_copy) > 1 and char_num_copy.index('十')==len(char_num_copy)-1:
                    char_num_copy = char_num_copy.replace('十', '0')
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
        elif limit_word in ["前"]:
            add_num = -2
        elif limit_word in ["后"]:
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
        if result_limit in ["下午", "晚饭时间", "黄昏", "晚上", "晚", "午夜", "夜间","夜里", "黑夜"] \
                and result_hour < 12:
            result_hour = result_hour+12
        else:
            result_hour = result_hour
        if result_min:
            result_min1 = self.get_num_from_char(result_min)
            result_min1 = result_min1.replace("分", "").replace("半", "30").replace('刻','')
            if '刻' in result_min:
                result_min = int(result_min1)*15
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
        now_time = datetime.datetime.now()
        regex_1 = "((?:(%s+)|(%s))年)?(%s+月)?(%s+)[日|号|天]?([后前])?" \
                  % (self.number_word, self.time_limit_word, self.number_word, self.number_word)
        regex_2 = "({time_limit_word})?个?(周|礼拜|星期)({number_word}+)". \
            format(time_limit_word=self.time_limit_word, number_word=self.number_word)
        regex_3 = "({time_limit_word})个?(日|天|早|晚|夜)". \
            format(time_limit_word=self.time_limit_word)
        # 2017年8月10号
        pattern_1 = re.compile(regex_1).search(text)
        # 下个周三
        pattern_2 = re.compile(regex_2).search(text)
        # 明天
        pattern_3 = re.compile(regex_3).search(text)

        if pattern_1:
            year_word = pattern_1.group(1)
            month_word = pattern_1.group(4)
            day_word = pattern_1.group(5)
            time_limit = pattern_1.group(6)

            # year
            if year_word:
                year = year_word.replace("年", "")
                if year in self.time_limit_word:
                    add_num = self.get_num_from_time_unit(year)
                    year = now_time.year+add_num
                else:
                    year = self.get_num_from_char(year)
                    # if len(year) < 2:
                    #     print("year is wrong: %s" % year)
                    #     year = now_year
                    # elif len(year) == 2:
                    #     year = int(str(now_year)[0:2]+year)
                    #     if year > now_year:
                    #         year = year - 100
                    # elif len(year) == 3:
                    #     year = now_year
                    # elif len(year) > 4:
                    #     year = now_year
                    # else:
                    #     year = int(year)
                    if len(year) == 2:
                        year = int(str(now_time.year)[0:2]+year)
                        if year > now_time.year:
                            year = year - 100
                    else:
                        year = int(year)
                        if year > 9999:
                            year = 9999
            else:
                year = now_time.year
            # month
            if month_word:
                month_word = month_word.replace("月", "")
                month_word = self.get_num_from_char(month_word)
                month = int(month_word)
            else:
                month = now_time.month
            if month > 12 or month == 0:
                print("month is wrong: %s" % str(month))
                month = 12 if month > 12 else 1
            # day
            day_word = self.get_num_from_char(day_word)
            day = int(day_word)
            if day == 0 or day > calendar.monthrange(year, month)[1]:
                print("day is wrong: %s" % str(day))
                day = calendar.monthrange(year, month)[1] if day > calendar.monthrange(year, month)[1] else 1
            if time_limit in ['前', '后']:
                if time_limit =='后':
                    normal_date = datetime.datetime.now()+ datetime.timedelta(days=day)
                if time_limit =='前':
                    normal_date = datetime.datetime.now() + datetime.timedelta(days= day*(-1))
            else:
                normal_date = datetime.datetime(year, month, day).date()
            time_str = pattern_1.group()
            return time_str, normal_date
        elif pattern_2 or pattern_3:
            pattern_23 = pattern_2 if pattern_2 else pattern_3
            limit_word = pattern_23.group(1)
            unit_word = pattern_23.group(2)

            else_word = ''
            try:
                num_word = pattern_23.group(3)
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
                    base_date = now_time-datetime.timedelta(days=weekday)
                    add_num = add_num*7
                elif unit_word in ["日", "天", "早", "晚", "夜"]:
                    base_date = now_time
                    add_num = add_num*1
            if num_word:
                num = self.char2num.get(num_word, num_word)
                try:
                    num = int(num)
                    if num > 7:
                        num = num/10
                except Exception as e:
                    print(e)
                    print("error: 时间点中的数字转换出问题")
                    num = None
            if num:
                base_date = base_date+datetime.timedelta(days=num)
            normal_date = base_date + datetime.timedelta(days=add_num)
            if else_word:
                a = pattern_23.group().replace(else_word,'')
            else:
                a = pattern_23.group()
            time_str = re.split("{number_word}".format(number_word=self.number_word), pattern_23.group())
            time_str = a[a.index(time_str[0][-1]):a.index(time_str[0][-1])+2]
            for x in ["早", "晚", "夜"]:
                time_str = a.replace(x, "")
            return time_str, normal_date.date()
        else:
            return "", ""

    def get_tpt(self, text):
        """
        Extracting time point intra-day!
        
        :return: 
        """
        now_time = datetime.datetime.now()
        # get day time
        day_time = self.get_day(text)
        day_str = day_time[0]
        day_normal_time = day_time[1]
        if day_str and day_normal_time:
            regex = "({day_str})({time_intra})?({number_word}+)(时|点|:|：)(({number_word}+))?(半)?". \
                format(day_str=day_str, time_intra=self.time_intra, number_word=self.number_word)
            pattern = re.compile(regex).search(text)
            if pattern:
                result_limit = pattern.group(2)
                result_hour = pattern.group(3)
                result_min = pattern.group(5) if pattern.group(5) else pattern.group(7)
                # replace with num
                result_hour, result_min = self.parsing_hour_min(result_hour, result_min, result_limit)
                tpt_normal = datetime.datetime(day_normal_time.year, day_normal_time.month, day_normal_time.day
                                               , result_hour, result_min, 0)
                tpt_str = pattern.group()
                return {"tpt": tpt_str, "tpt_normal": tpt_normal.strftime("%Y-%m-%d %H:%M:%S")}
            else:
                return {"tpt": day_str, "tpt_normal": day_normal_time.strftime("%Y-%m-%d")}
        else:
            # 下午5点
            regex_1 = "({time_intra})?({number_word}+)(点|时|:|：)(({number_word}+)?([分刻]?))?(半)?". \
                format(time_intra=self.time_intra, number_word=self.number_word)
            # 三天后
            regex_2 = "(({number_word}+)个?(天|日|周|礼拜|星期|年|月)后)|(过个?({number_word}+)(天|日|周|礼拜|星期|年|月))". \
                format(number_word=self.number_word)
            # 3分钟后, 3个钟头后
            # regex_3 = ur"(({number_word}+)个?半?(分钟?|小时|钟头?|刻钟?)后)|(过个?({number_word}+)个?半?(分钟?|小时|钟头?|刻钟?))"\
            #     .format(number_word=self.number_word)
            regex_3 = "({number_word}+)个?半?(分钟?|小时|钟头?|刻钟?)(({number_word}+)(?:分|刻))?" \
                .format(number_word=self.number_word)

            # TODO : 3hours5minutes
            pattern_1 = re.compile(regex_1).search(text)
            pattern_2 = re.compile(regex_2).search(text)
            pattern_3 = re.compile(regex_3).search(text)
            if pattern_1:
                result_hour = pattern_1.group(2)
                result_limit = pattern_1.group(1)
                result_min = pattern_1.group(4) if pattern_1.group(4) else pattern_1.group(6)
                result_hour, result_min = self.parsing_hour_min(result_hour, result_min, result_limit)
                tpt_normal = datetime.datetime(now_time.year, now_time.month, now_time.day,
                                               result_hour, result_min, 0)
                tpt_str = pattern_1.group()
                if not result_limit:
                    if tpt_normal < now_time:
                        tpt_normal = tpt_normal + datetime.timedelta(hours=12)
                return {"tpt": tpt_str, "tpt_normal": tpt_normal.strftime("%Y-%m-%d %H:%M:%S")}

            elif pattern_2:
                try:
                    result_num = pattern_2.group(2)
                    result_unit = pattern_2.group(3)
                    num = int(self.get_num_from_char(result_num))
                except:
                    result_num = pattern_2.group(5)
                    result_unit = pattern_2.group(6)
                    num = int(self.get_num_from_char(result_num))
                if result_unit in ["星期", "周", "礼拜"]:
                    num = num*7
                if result_unit in ["日", "天"]:
                    num = num*1
                if result_unit in ["年"]:
                    num = num*365
                if result_unit in ["月"]:
                    num = num*30
                tpt_normal = now_time.date() + datetime.timedelta(days=num)
                tpt_str = pattern_2.group()
                return {"tpt": tpt_str, "tpt_normal": tpt_normal.strftime("%Y-%m-%d")}
            elif pattern_3:
                pattern_temp = pattern_3.group()
                result_num = pattern_3.group(1)
                result_unit = pattern_3.group(2)
                minute_st = pattern_3.group(3)
                minute_num = pattern_3.group(4)
                result_num = self.get_num_from_char(result_num)
                if result_num == "半":
                    num = 0.5
                    pattern_temp = pattern_3.group().replace("半", "")
                else:
                    num = int(result_num)
                if result_unit in ["分", "分钟"]:
                    num = num*1
                if result_unit in ["小时", "钟", "钟头"]:
                    num = num*60
                    if "半" in pattern_temp:
                        num = num + 30
                if result_unit in ["刻", "刻钟"]:
                    num = num*15
                if minute_st and result_unit in ["小时", "钟", "钟头"]:
                    minute_num = self.get_num_from_char(minute_num)
                    minute_num = int(minute_num)
                    num = num + minute_num
                elif minute_st:
                    print("two tpt: error!")
                    return {"tpt": "", "tpt_normal": ""}
                tpt_normal = now_time + datetime.timedelta(minutes=num)
                tpt_str = pattern_3.group()
                return {"tpt": tpt_str, "tpt_normal": tpt_normal.strftime("%Y-%m-%d %H:%M:%S")}
            else:
                return {"tpt": "", "tpt_normal": ""}

    def get_day_period(self, text):
        """
        Extracting time period! 
        
        :param text: 
        :return: 
        """
        start_date_str  =''
        end_date_str = ''
        now_date = datetime.datetime.now()
        regex = "({time_limit_word})个?(年|月|周|礼拜|星期)".format(time_limit_word=self.time_limit_word)
        pattern = re.compile(regex).search(text)
        if pattern:
            limit_word = pattern.group(1)
            tpd_word = pattern.group(2)
            add_num = 0
            if limit_word:
                add_num = self.get_num_from_time_unit(limit_word)
            if tpd_word:
                if tpd_word in ["星期", "周", "礼拜"]:
                    weekday = datetime.datetime.now().isoweekday()
                    start_date = now_date-datetime.timedelta(days=weekday-1)
                    end_date = start_date + datetime.timedelta(days=6)
                    add_num = add_num*7
                    start_date = start_date + datetime.timedelta(days=add_num)
                    end_date = end_date + datetime.timedelta(days=add_num)
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    end_date_str = end_date.strftime("%Y-%m-%d")
                elif tpd_word in ["月"]:
                    last_day = calendar.monthrange(now_date.year, now_date.month+add_num)[1]
                    start_day = 1
                    start_date = datetime.date(now_date.year, now_date.month+add_num, start_day)
                    end_date = datetime.date(now_date.year, now_date.month+add_num, last_day)
                    # add_num = add_num*last_day
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    end_date_str = end_date.strftime("%Y-%m-%d")
                elif tpd_word in ["年"]:
                    leap_flag = calendar.isleap(now_date.year+add_num)
                    if leap_flag:
                        year_day = 366
                    else:
                        year_day = 365
                    start_day = 1
                    start_date = datetime.date(now_date.year+add_num, 1, start_day)
                    end_date = start_date + datetime.timedelta(days=year_day-1)
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    end_date_str = end_date.strftime("%Y-%m-%d")
            time_str = pattern.group()
            return {"tpd": time_str,
                    "tpd_start": start_date_str,
                    "tpd_end": end_date_str}
        else:
            return {"tpd": "",
                    "tpd_start": "",
                    "tpd_end": ""}

    def get_tpd_intra_day(self, text):
        """
        Extracting intra-day time period!
        
        :param text: 
        :return: 
        """
        now_time = datetime.datetime.now()
        # get day time
        day_time = self.get_day(text)
        day_str = day_time[0]
        day_normal_time = day_time[1]
        if day_str and day_normal_time:
            regex = "({tpt_str})({time_intra})".format(tpt_str=day_str, time_intra=self.time_intra)
            pattern = re.compile(regex).search(text)
            if pattern:
                result_limit = pattern.group(2)
                time_period =[]
                for x in self.time_intra_day:
                    if re.compile(self.time_intra_day[x]).search(result_limit):
                        time_period.append(x)
                if time_period:
                    time_period.sort(key=lambda x : len(x), reverse=True)
                    time_range = self.time_intra_day_range.get(time_period[0], "")
                    tpd_start = 0
                    day_add = 0
                    tpd_end = 0
                    if time_range:
                        tpd_start = time_range[0]
                        tpd_end = time_range[1]
                        if time_period[0] in ["晚上"]:
                            day_add = 1
                        else:
                            day_add = 0
                    date_st_start = datetime.datetime(day_normal_time.year, day_normal_time.month, day_normal_time.day, tpd_start, 0, 0)
                    date_st_end = datetime.datetime(day_normal_time.year, day_normal_time.month, day_normal_time.day+ day_add, tpd_end, 0, 0)
                    return {"tpd": pattern.group(),
                            "tpd_start": date_st_start.strftime("%Y-%m-%d %H:%M:%S"),
                            "tpd_end": date_st_end.strftime("%Y-%m-%d %H:%M:%S")}
                else:
                    return {"tpd": "",
                            "tpd_start": "",
                            "tpd_end": ""}
            else:
                return {"tpd": "",
                        "tpd_start": "",
                        "tpd_end": ""}
        else:
            regex = "({time_intra})".format(time_intra=self.time_intra)
            pattern = re.compile(regex).search(text)

            if pattern:
                result_limit = pattern.group(1)
                time_period =[]
                for x in self.time_intra_day:
                    if re.compile(self.time_intra_day[x]).search(result_limit):
                        time_period.append(x)
                if time_period:
                    time_period.sort(key=lambda x : len(x), reverse=True)
                    time_range = self.time_intra_day_range.get(time_period[0], "")
                    if time_range:
                        tpd_start = time_range[0]
                        tpd_end = time_range[1]
                        if time_period[0] in ["晚上"]:
                            day_add = 1
                        else:
                            day_add = 0
                        date_st = datetime.datetime.now()
                        date_st_start = datetime.datetime(date_st.year,date_st.month,date_st.day, tpd_start, 0, 0)
                        date_st_end = datetime.datetime(date_st.year,date_st.month,date_st.day+day_add, tpd_end, 0, 0)
                        return {"tpd": pattern.group(),
                                "tpd_start": date_st_start.strftime("%Y-%m-%d %H:%M:%S"),
                                "tpd_end": date_st_end.strftime("%Y-%m-%d %H:%M:%S")}
                    else:
                        return {"tpd": "",
                                "tpd_start": "",
                                "tpd_end": ""}
                else:
                    return {"tpd": "",
                            "tpd_start": "",
                            "tpd_end": ""}
            else:
                return {"tpd": "",
                        "tpd_start": "",
                        "tpd_end": ""}

    def get_tfy_day(self, text):
        """
        Extracting time frequency!
        
        :param text: 
        :return: 
        """
        now_time = datetime.datetime.now()
        regex = "({frequency_word})({number_word})?个?(年|月|周|礼拜|星期|天|日)的?({number_word}+)?月?的?({number_word}+)?[日号]?". \
            format(frequency_word=self.frequency_word, number_word=self.number_word)
        pattern = re.compile(regex).search(text)
        if pattern:
            num_word = pattern.group(2)
            time_word = pattern.group(3)
            num_word_1 = pattern.group(4)
            num_word_2 = pattern.group(5)
            num = None
            if not num_word and time_word == "年" and num_word_1 and num_word_2 :
                num_word_1 = self.get_num_from_char(num_word_1)
                num_word_2 = self.get_num_from_char(num_word_2)

                start_time = datetime.datetime(now_time.year, int(num_word_1), int(num_word_2))
                frequency = 1
                f_unit = "Y"
                return {"tfy": pattern.group(),
                        "start_time": start_time.strftime("%Y-%m-%d"),
                        "frequency": frequency,
                        "f_unit": f_unit
                        }
            elif not num_word and time_word == "年" and num_word_1 and not num_word_2:
                num_word_1 = self.get_num_from_char(num_word_1)
                start_time = datetime.datetime(now_time.year, int(num_word_1), 1)
                frequency = 12
                f_unit = "m"
                return {"tfy": pattern.group(),
                        "start_time": start_time.strftime("%Y-%m-%d"),
                        "frequency": frequency,
                        "f_unit": f_unit
                        }
            elif not num_word and time_word == u"月" and num_word_1 and not num_word_2:
                num_word_1 = self.get_num_from_char(num_word_1)
                start_time = datetime.datetime(now_time.year, now_time.month, int(num_word_1))
                frequency = 1
                f_unit = "m"
                return {"tfy": pattern.group(),
                        "start_time": start_time.strftime("%Y-%m-%d"),
                        "frequency": frequency,
                        "f_unit": f_unit
                        }
            elif not num_word and time_word in ["周", "礼拜", "星期"] and num_word_1 and not num_word_2:
                num_word_1 = self.get_num_from_char(num_word_1)
                weekday = now_time.isoweekday()
                base_date = now_time-datetime.timedelta(days=weekday)
                start_time = base_date + datetime.timedelta(days=int(num_word_1))
                frequency = 7
                f_unit = "d"
                return {"tfy": pattern.group(),
                        "start_time": start_time.strftime("%Y-%m-%d"),
                        "frequency": frequency,
                        "f_unit": f_unit
                        }
            elif time_word and not num_word_1 and not num_word_2:
                frequency = 1
                f_unit = "d"
                if time_word in ["天", "日"]:
                    f_unit = "d"
                    frequency = 1
                elif time_word in ["周", "礼拜", "星期"]:
                    f_unit = "d"
                    frequency = 7
                elif time_word in ["月"]:
                    f_unit = "m"
                    frequency = 1
                elif time_word in ["年"]:
                    f_unit = "Y"
                    frequency = 1
                if num_word:
                    num = self.char2num.get(num_word, num_word)
                    try:
                        num = int(num)
                    except Exception as e:
                        print.error(e)
                        print("error: 时间点中的数字转换出问题")
                        num = None
                if num:
                    frequency = frequency * num

                return {"tfy": pattern.group(),
                        "start_time": now_time.strftime("%Y-%m-%d"),
                        "frequency": frequency,
                        "f_unit": f_unit}
            else:
                return {"tfy": "",
                        "start_time": "",
                        "frequency": "",
                        "f_unit": ""}

        else:
            return {"tfy": "",
                    "start_time": "",
                    "frequency": "",
                    "f_unit": ""}

    def get_tfy_repeat(self, text):
        """
        Extracting time frequency in a Day!
        
        :param text: 
        :return: 
        """
        now_time = datetime.datetime.now()
        # get day time
        day_time = self.get_day(text)
        day_str = day_time[0]
        day_normal_time = day_time[1]
        if day_str and day_normal_time:
            regex = "每个?({tpt_str})({time_intra})?(({number_word}+)(?:点|时)半?)(({number_word}+)分?)?". \
                format(tpt_str=day_str, time_intra=self.time_intra, number_word=self.number_word)
            pattern = re.compile(regex).search(text)
            if pattern:
                result_limit = pattern.group(2)
                result_hour = pattern.group(4)
                result_min = pattern.group(5)
                result_hour, result_min = self.parsing_hour_min(result_hour, result_min, result_limit)
                if '半' in pattern.group(3):
                    result_min = result_min + 30
                date_st = datetime.datetime(day_normal_time.year, day_normal_time.month, day_normal_time.day, result_hour, result_min, 0)

                if "周" in day_str or "礼拜" in day_str or "星期" in day_str:
                    day_frequency = 7
                else:
                    day_frequency = 1
                return {"tfy": pattern.group(),
                        "start_time": date_st.strftime("%Y-%m-%d %H:%M:%S"),
                        "frequency": day_frequency,
                        "f_unit": "d"}
            else:
                return {"tfy": "",
                        "start_time": "",
                        "frequency": "",
                        "f_unit": ""}
        else:
            regex = "每(?![天日])[相间]?[隔过]?(([0-9半]+).{0,3}[时钟]头?)?(([0-9]+)分)?"
            pattern = re.compile(regex).search(text)
            regex_1 = "每[相间]?[隔过个]?({time_intra})".format(time_intra= self.time_intra)
            pattern_1 = re.compile(regex_1).search(text)
            regex_2 = "每[日天]({time_intra})({number_words}+)[点时]({number_words}+)?[分半]?". \
                format(time_intra=self.time_intra, number_words=self.number_word)
            pattern_2 = re.compile(regex_2).search(text)
            if pattern_1:
                time_intra_temp = pattern_1.group(1)
                time_intra = ""
                time_period =[]
                for x in self.time_intra_day:
                    if re.compile(self.time_intra_day[x]).search(time_intra_temp):
                        time_period.append(x)
                if time_period:
                    time_period.sort(key=lambda x : len(x), reverse=True)
                    day_range = self.time_intra_day_range.get(time_period[0], "")
                    if day_range:
                        start_hour = int(day_range[0])
                        if time_period[0] in ["晚上"]:
                            day_add = 1
                        else:
                            day_add = 0
                        start_time = datetime.datetime(now_time.year, now_time.month, now_time.day, start_hour)
                        return {"tfy": pattern_1.group(),
                                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "frequency": 1,
                                "f_unit": "d"}
                    else:
                        return {"tfy": "",
                                "start_time": "",
                                "frequency": "",
                                "f_unit": ""}
            elif pattern:
                pattern_temp = pattern.group()
                result_1 = pattern.group(1)
                result_2 = pattern.group(3)
                total_min = 0
                if result_1 and result_2:
                    try:
                        result_min_1 = int(pattern.group(2))*60
                    except:
                        result_min_1 = 30
                        pattern_temp = pattern_temp.replace("半", "")
                    if "半" in pattern_temp:
                        result_min_1 = result_min_1 + 30
                    result_min_2 = int(pattern.group(4))
                    total_min = result_min_1 + result_min_2
                if result_1 and not result_2:
                    if "小时" in result_1 or "钟头" in result_1:
                        try:
                            result_min_1 = int(pattern.group(2))*60
                        except:
                            result_min_1 = 30
                            pattern_temp = pattern_temp.replace("半", "")
                        if "半" in pattern_temp:
                            result_min_1 = result_min_1 + 30
                        total_min = result_min_1
                    elif "分" in result_1:
                        total_min = int(pattern.group(2))
                    try:
                        return {"tfy": pattern.group(),
                                "start_time": now_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "frequency": total_min,
                                "f_unit": "M"}
                    except Exception as e:
                        print("RE error!" + e.message)
                        return {"tfy": "",
                                "start_time": "",
                                "frequency": "",
                                "f_unit": ""}
                else:
                    return {"tfy": "",
                            "start_time": "",
                            "frequency": "",
                            "f_unit": ""}
            elif pattern_2:
                result_limit = pattern_2.group(1)
                result_hour = pattern_2.group(2)
                result_min = pattern_2.group(3)
                result_hour, result_min = self.parsing_hour_min(result_hour, result_min, result_limit)
                if '半' in pattern_2.group():
                    result_min = result_min + 30
                date_st = datetime.datetime(now_time.year, now_time.month, now_time.day, result_hour, result_min, 0)
                day_frequency = 1
                return {"tfy": pattern_2.group(),
                        "start_time": date_st.strftime("%Y-%m-%d %H:%M:%S"),
                        "frequency": day_frequency,
                        "f_unit": "d"}
            else:
                return {"tfy": "",
                        "start_time": "",
                        "frequency": "",
                        "f_unit": ""}

    def get_uncertain_time(self, text):
        """
        Extracting uncertain time!
        
        :return: 
        """
        pattern = self.reg_uncertain_time.search(text)
        if pattern:
            return pattern.group()
        else:
            return ""

    def extracter(self, text):
        """
        Main function!
        
        :param text: 
        :return: 
        """
        try:
            # 抽取不确定的时间
            uc_json = self.get_uncertain_time(text)
            #
            tpt_json = self.get_tpt(text)
            #
            tpd_day_json = self.get_day_period(text)
            tpd_intra_json = self.get_tpd_intra_day(text)
            if tpd_intra_json["tpd"]:
                tpd_json = tpd_intra_json
            else:
                tpd_json = tpd_day_json
            tfy_day = self.get_tfy_day(text)
            tfy_min = self.get_tfy_repeat(text)

            if tfy_min["tfy"]:
                tfy_json = tfy_min
            else:
                tfy_json = tfy_day
            # eliminating duplicates

            time_str = [tpt_json["tpt"], tpd_json["tpd"], tfy_json["tfy"]]
            time_str_base = ""
            for x in time_str:
                if x:
                    if not time_str_base:
                        time_str_base = x
                    else:
                        if time_str_base in x:
                            time_str_base = x
            if tpt_json["tpt"] or tpd_json["tpd"] or tfy_json["tfy"]:
                if tpt_json["tpt"] == time_str_base:
                    # for x in tpd_json:
                    #     tpd_json[x] = ""
                    # for y in tfy_json:
                    #     tfy_json[y] = ""
                    tpd_json = ""
                    tfy_json = ""
                    return TimeSlot({"tpt": tpt_json, "tpd": tpd_json, "tfy": tfy_json, "uc": uc_json})
                if tpd_json["tpd"] == time_str_base:
                    # for x in tpt_json:
                    #     tpt_json[x] = ""
                    # for y in tfy_json:
                    #     tfy_json[y] = ""
                    tpt_json = ""
                    tfy_json = ""
                    return TimeSlot({"tpt": tpt_json, "tpd": tpd_json, "tfy": tfy_json, "uc": uc_json})
                if tfy_json["tfy"] == time_str_base:
                    # for x in tpt_json:
                    #     tpt_json[x] = ""
                    # for y in tpd_json:
                    #     tpd_json[y] = ""
                    tpt_json = ""
                    tpd_json = ""
                    return TimeSlot({"tpt": tpt_json, "tpd": tpd_json, "tfy": tfy_json, "uc": uc_json})
            else:
                return TimeSlot({"tpt": "", "tpd": "", "tfy": "", "uc": uc_json})
        except Exception as e:
            print("Time Module error:" + e.message)
            return TimeSlot({"tpt": "", "tpd": "", "tfy": "", "uc": ""})

time_extractor = TimeSlotExtracter()

if __name__ == "__main__":
    # file_path = "amber/memory/memory_qa/time_text"
    # f_w_path = "amber/memory/memory_qa/time_text_out"
    # f_w = open(f_w_path, "w+")
    # with open(file_path) as f:
    #     line = f.readline()
    #     line = line.strip()
    #     while line:
    #         if type(line).__name__ == "str":
    #             line = line.decode("utf-8
    #
    # ")
    #         time_module = TimeModule()
    #         json_out = time_module.time_process(line)
    #         json_out = str(json_out).decode("utf-8")
    #         out_str = (line + "@" + json_out).encode("utf-8")
    #         f_w.writelines(out_str+"\n")
    #         print line + u"  " + json_out
    #         line = f.readline()
    #         line = line.strip()
    # text = u"我9点一刻去上海"
    # {'tpt': {'tpt': '9\xe7\x82\xb9\xe4\xb8\x80\xe5\x88\xbb', 'tpt_normal': '2017-07-23 21:15:00'}, 'tfy': '', 'uc': '',
    #  'tpd': ''}
    # {'tpt': '9\xe7\x82\xb9\xe4\xb8\x80\xe5\x88\xbb', 'tpt_normal': '2017-07-23 21:15:00'}
    # text = u'设置7月30日的闹钟'
    # {'tpt': {'tpt': '7\xe6\x9c\x8830\xe6\x97\xa5', 'tpt_normal': '2017-07-30'}, 'tfy': '', 'uc': '', 'tpd': ''}
    # {'tpt': '7\xe6\x9c\x8830\xe6\x97\xa5', 'tpt_normal': '2017-07-30'}
    # text =  u'每天早上9点的闹钟'
    # {'tpt': '', 'tfy': {'f_unit': 'd', 'start_time': '2017-07-23 09:00:00', 'frequency': 1,
    #                     'tfy': '\xe6\xaf\x8f\xe5\xa4\xa9\xe6\x97\xa9\xe4\xb8\x8a9\xe7\x82\xb9'}, 'uc': '', 'tpd': ''}
    # text = u"设置每周三下午6点半的闹钟"# 19号已经过去了，需要设置成26号比较好。
    # {'tpt': '', 'tfy': {'f_unit': 'd', 'start_time': '2017-07-19 18:30:00', 'frequency': 7,
    #                     'tfy': '\xe6\xaf\x8f\xe5\x91\xa8\xe4\xb8\x89\xe4\xb8\x8b\xe5\x8d\x886\xe7\x82\xb9\xe5\x8d\x8a'},
    #  'uc': '', 'tpd': ''}
    text = "明天上午9点"#u"设置每周一至周五8点半的闹钟"
    # {'tpt': '',
    #  'tfy': {'f_unit': 'd', 'start_time': '2017-07-17', 'frequency': 7, 'tfy': '\xe6\xaf\x8f\xe5\x91\xa8\xe4\xb8\x80'},
    #  'uc': '', 'tpd': ''}
    time_module = TimeSlotExtracter()
    result = time_module.extracter(text)
    # print(result.value)
    import json
    print(json.dumps(result.value, ensure_ascii=False, indent=4))
    if result.value.get('tpt', ''):
        print(result.value.get('tpt', ''))
        print('ok')
    else:
        print('false')
# uc：不确定的时间u"我马上就要出去了"
# tpt：时间点u"今天下午6点半提醒我出去"
# tfy：频率u"每周三提醒我出去"
# tpd：时间段u"下个月提醒我出去"