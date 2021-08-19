#!/usr/bin/env python
# -*- coding:utf8 -*-
import re
from util.trie_match import trie_tree
# from util.tools import util
from template_match.reg_util import *
from util.slot_extracter.get_day import time_extractor
import util.slot_extracter.deal_age as deal_age
import util.slot_extracter.deal_height as deal_height



class ArgsDisambiguation:
    def __init__(self):
        self.trie_matcher = trie_tree
        self.age_map = {}

    def check_args_compatibility(self, rel_candidate, sent):
        """
        归一候选关系的args，并通过args做关系消歧
        :param rel_candidate: 候选关系列表
        :param sent: 输入语句
        :return: (compatibility, normalized_args), 其中compatibility是布尔型，True表示args和关系兼容、False表示args和关系不兼容
        """
        arg1 = rel_candidate['extract_arg1']
        arg2 = rel_candidate['extract_arg2']
        arg3 = rel_candidate['extract_arg3']
        if re.search(reg_what, sent) or arg2 in ["是", "叫", "叫做", "呢", "在", "做"] or arg2 == "x?":
            arg4 = 'x?'
        else:
            arg4 = 'x'
        rel = rel_candidate['rel']  # [0]
        args = [arg1, arg2, arg3, arg4]
        # 根据关系类型生成相应的方法
        check_method_name = "_check_" + rel + "_arg"
        # normalize_method_name = "_normalize_" + rel + "_args"
        # print('!!!!!!', check_method_name,normalize_method_name)
        # 检查ArgsHandling类是否实现了对应的check和normalize方法，并返回方法名
        try:
            check_method = getattr(ArgsDisambiguation, check_method_name)
        except AttributeError:
            return False, []

        compatibility = check_method(self, args, sent)  # 根据归一后的args来判断兼容性
        return compatibility, args


    def _normalize_arg(self, arg):
        """
        对正则抠取的表示琥珀或用户的字符串做归一化
        :param arg: 关系三元组中的arg1或arg2
        :return: 归一化的arg，如果arg不是表示琥珀或用户的，则不做任何变更，直接返回arg
        """
        # arg = util.check_unicode(arg)
        return arg

    def _check_gender_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if "处" == arg[0]:
            return False
        pattern_1 = "父母|母亲|父亲|母校|作者|书名|出版社|出版|版本|版次|版|开本|页数|译者|翻译|字数|纸张|装帧|实施"
        if re.search(pattern_1, sent):
            return False
        match_male = re.search(reg_male, arg[1])
        match_ad_male = re.search(reg_ad_male, arg[1])
        match_female = re.search(reg_female, arg[1])
        match_ad_female = re.search(reg_ad_female, arg[1])
        regex_1 = u'(.+)是(.+)'
        if re.search(regex_1, arg[0]):
            return False
        if match_male or match_ad_male:
            arg[1] = u'male'
        elif (match_female or match_ad_female):
            arg[1] = u'female'
        else:
            arg[1] = u'x?'
        return True

    def disambiguation_gender(self, triple, sent):
        '''
        属性"性别"的消歧处理
        :param triple: 输入一个提取的三元组
        :param sent: 输入的句子
        :return: 返回结果为两个：一是该三元组是否符合gender属性，
                 二是消歧过后的三元组信息
        '''
        # 排除subject词和object提取内容错误的情况，例如将属性值匹配到了subject和object槽位的情况
        if re.search(attributes_regex, triple['object']) or re.search(attributes_regex, triple['subject']):
            return [False, {}]
        # 排除subject词是一些无意义的表述的情况
        if re.search(general_pattern, triple['subject']):
            return [False, {}]
        match_male = re.search(reg_male, triple['object'])
        match_female = re.search(reg_female, triple['object'])
        # 排除主体词提取错误的情况
        regex_1 = '(.+)是(.+)'
        if re.search(regex_1, triple['subject']):
            return [False, {}]
        if match_male :
            triple['object'] = '男'
        elif match_female:
            triple['object'] = '女'
        else:
            triple['object'] = 'x?'

        return True, triple


    def _normalize_gender_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_age_arg(self, arg, sent):
        pattern_1 = "身高|身高|个头|个子|身长|高度|体重数?|重量|(斤|千克)数|米|厘米|千克|克|斤|员工|页|字|纸张|绿化率|容积率|户"
        if re.search(pattern_1, sent):
            return False
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        time_replace = "现在|将来|过去|实际|多大"
        arg[0] = re.sub(time_replace, '', arg[0])
        if arg[1] in deal_age.age_type_1:
            arg[1] = deal_age.age_type_1.get(arg[1], 'x?')
        elif (arg[1] in deal_age.age_type_2):
            arg[1] = deal_age.age_type_2.get(arg[1], 'x?')
        elif ("奔" in arg[1]):
            arg[1] = deal_age.age_type_3(arg[1])
        else:
            candidate = cn2dig(arg[1])
            match_number = re.search(r"\d+", candidate)
            if match_number:
                number = match_number.group()
                if "多" in arg[1]:
                    arg[1] = str(number) + '-' + str(int(number) + 10)
                elif ("超过" in arg[1] or "超" in arg[1] or "过了" in arg[1] or "以上" in arg[1]):
                    arg[1] = str(number) + '-'
                elif ("低于" in arg[1] or "以下" in arg[1]):
                    arg[1] = '-' + str(number)
                else:
                    arg[1] = number
        return True

    def _normalize_age_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_jobTitle_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if arg[1] == "":
            return False
        pattern_1 = "部门|职务|职责|角色|荣誉|荣耀|荣誉奖|成立|建立|创办|公司|企业|上市|代表|类型|出版|版本|版次|版|翻译|物业|学科|纲|目|科|类|界|简称|全称|领域"
        if re.search(pattern_1, sent):
            return False
        arg[1] = arg[1].replace("吗", "")
        arg[0] = arg[0].replace("还在", "")
        arg[0] = arg[0].replace("现在", "")

        replace_unit = ["职业", "工作", "工种"]
        for unit in replace_unit:
            arg[1] = arg[1].replace(unit, "")
            arg[0] = arg[0].replace(unit, "")
        if re.search(reg_what, arg[1]):
            arg[1] = "x?"
        if arg[0]:
            if arg[0][-1] == "变" and "变成" in sent:
                arg[0] = arg[0][:-1]
        if arg[1] == "x?":
            return True
        else:
            trie_result = self.trie_matcher.trie_match(arg[1])
            if "occupation" in trie_result:
                if "position" in trie_result:
                    return False
                else:
                    arg[1] = trie_result["occupation"][0]
                    arg[1] = arg[1].replace("的", "")
                    return True
            else:
                return False

    def _normalize_jobTitle_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_bloodType_arg(self, arg, sent):
        if arg[1].isalpha():
            arg[1] = arg[1].upper()
        blood_type = "A|B|AB|O|a|b|ab|o"
        if re.search(blood_type, arg[0]):
            return False
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if "AB" in sent:
            arg[1] = "AB型"
        arg[0] = arg[0].replace("血型", "")
        if re.search(reg_blood, arg[1]):
            arg[1] = (re.search(reg_blood, arg[1])).group(0)
            arg[1] = arg[1].upper() + "型"
            return True
        else:
            arg[1] = "x?"
            return True

    def _normalize_bloodType_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_birthDate_arg(self, arg, sent):
        pattern_1 = "(1|2|3|4|5|6|7|8|9|10|11|12|一|二|三|四|五|六|七|八|九|十|十一|十二)月$"
        pattern_2 = "1|2|3|4|5|6|7|8|9|10|11|12"
        pattern_3 = u'哪里|什么地方|出生地|在哪'
        pattern_4 = u'\\d|一|二|三|四|五|六|七|八|九|十|十一|十二'
        arg[1] = cn2dig(arg[1])
        if re.search(pattern_1, arg[1]):
            arg[1] = arg[1] + u'份'
        if re.search(pattern_3, sent) and "在哪天" not in sent:
            return False
        arg[0] = arg[0].replace("具体", "")
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        sent = sent.replace(u'吗', '')
        if arg[0][-1].isdigit():
            number = arg[0][-1]
            arg[0] = arg[0].replace(number, "")
            arg[1] = str(number) + str(arg[1])
        if re.search(u'\\d+月\\d+号|\\d+月', arg[0]):
            return False
        if re.search(reg_what, sent):
            arg[1] = "x?"
        if arg[1] == "x?":
            return True
        if re.search(pattern_4, arg[1]) is None:
            return False
        if arg[1][-1].isdigit():
            arg[1] = arg[1] + u'日'
        time_rst = time_extractor.extracter(arg[1])
        # print('time_rst',time_rst.value)
        # print(type(time_rst))
        if 'tpt' in time_rst.value:
            time_slot = ''
            if 'tpt_normal' in time_rst.value['tpt'] and arg[2] != "constraint":
                time_slot = time_rst.value['tpt']['tpt_normal']
            if 'tpt' in time_rst.value['tpt'] and arg[2] != "constraint":
                # print(time_rst.value['tpt']['tpt'])

                time_slot_year = re.search('\d+',str(time_rst.value['tpt']['tpt'], encoding='utf8'))
                if time_slot_year:
                    time_slot_year = time_slot_year.group()
                    time_slot = time_slot_year + '/' + time_slot
            if arg[2] == 'constraint' and arg[1] == str(time_rst.value['tpt']['tpt'], encoding='utf8'):
                time_slot = time_rst.value['tpt']['tpt_normal']
            arg[1] = time_slot
        return True

    def _check_deathDate_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if "死党" in sent:
            return False
        if arg[0][-1] == "在":
            arg[0] = arg[0][:-1]
        if arg[0][-2:] == "方丈":
            arg[0] = arg[0][:-2]
        if len(arg[0]) >= 4 and arg[0][-1] == "才":
            arg[0] = arg[0][:-1]
        sent = sent.replace("吗", "")
        if arg[0]:
            if arg[0][-1].isdigit():
                number = arg[0][-1]
                arg[0] = arg[0].replace(number, "")
                arg[1] = str(number) + str(arg[1])
        if re.search(u'\\d+月\\d+号|\\d月', arg[0]):
            return False
        if re.search(reg_what, sent):
            arg[1] = "x?"
        if arg[1] == 'x?':
            return True
        else:
            time_rst = time_extractor.extracter(arg[1])
            if 'tpt' in time_rst.value:
                if 'tpt_normal' in time_rst.value['tpt'] and arg[2] != "constraint":
                    time_slot = time_rst.value['tpt']['tpt_normal'].decode('utf8')
                    arg[1] = time_slot
                    return True
                if arg[2] == "constraint" and arg[1] == time_rst.value['tpt']['tpt'].decode('utf8'):
                    time_slot = time_rst.value['tpt']['tpt_normal'].decode('utf8')
                    arg[1] = time_slot
                    return True

    def _normalize_height_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_height_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        sent = sent.replace("吗", "")
        sent = sent.replace("么", "")
        arg[1] = arg[1].replace("的", "")
        arg[0] = arg[0].replace("现在", "")
        if re.search("\\d+", arg[0]):
            return False
        if re.search(reg_what, sent):
            arg[1] = "x?"
        if arg[1] == "x?":
            return True
        else:
            arg[1] = deal_height.deal_height(arg[1])
            if arg[1] is not None:
                return True
            else:
                return False

    def _normalize_weight_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_weight_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        pattern_1 = "体重数?|重量|(斤|千克)数|身体体重|重约|重达"
        if re.search(pattern_1, arg[0]):
            return False
        sent = sent.replace("吗", "")
        sent = sent.replace("么", "")
        arg[0] = arg[0].replace(u'身体', '')
        arg[0] = arg[0].replace("现在", "")
        if re.search(u'斤|kg|千克', arg[0]):
            return False
        if re.search(reg_what, sent):
            arg[1] = "x?"
        if arg[1] == "x?":
            return True
        else:
            arg[1] = deal_height.deal_weight(arg[1])
            arg[1] = int(arg[1])//2
            return True

    def _normalize_achievement_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_achievement_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[0] = arg[0].replace("最大", "")
        arg[1] = re.sub(u'吗|呢', '', arg[1])
        pattern_1 = "作品|荣誉|荣耀|代表作|公司|页|字|翻译|物业|区"
        if re.search(pattern_1, sent):
            return False
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|何种|多细|怎样|哪个|哪些|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_works_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_works_arg(self, arg, sent):
        pattern_0 = ".+(是).+"
        if re.search(pattern_0, arg[0]):
            return False
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        pattern_1 = "成就|荣耀|荣誉|成果|贡献|提出|公司|企业|法定|页|字|翻译|物业|区"
        if re.search(pattern_1, sent):
            return False
        pattern_2 = "谁"
        if re.search(pattern_2, arg[1]):
            return False
        arg[1] = re.sub(u'吗|呢|么', '', arg[1])
        pattern_2 = "代表|主要|杰出"
        arg[0] = re.sub(pattern_2, "", arg[0])
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|何种|多细|怎样|哪个|哪些|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_honor_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_honor_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        pattern_1 = "作品|成就|提出|成果|贡献|代表作|成立|建立|创办|公司|企业|上市|代表|出版|版本|版次|版|页|字|翻译|物业|区|平装|线装|精装|.科.物|为了|所在地"
        if re.search(pattern_1, sent):
            return False
        arg[1] = re.sub(u'吗|呢', '', arg[1])
        if "荣誉" in arg[1] or "荣耀" in arg[1]:
            return False
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|何种|多细|怎样|哪个|哪些|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_birthDate_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _normalize_deathDate_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_constellation_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if re.search(reg_constellation, arg[0]):
            return False
        if re.search(reg_constellation, arg[1]):
            arg[1] = (re.search(reg_constellation, arg[1])).group(0)
            arg[1] = arg[1] + u'座'
            return True
        else:
            arg[1] = "x?"
            return True

    def _normalize_constellation_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_nationality_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        replace_word = "属不"
        pattern_0 = "隶属|前身|影响"
        arg[0] = re.sub(replace_word, "", arg[0])
        if re.search(pattern_0, sent):
            return False
        if "人" in arg[1]:
            arg[1] = arg[1].replace("人", "")
        if arg[1] != "x?":
            trie_result = self.trie_matcher.trie_match(arg[1])
            if "country" in trie_result:
                arg[1] = trie_result["country"][0]
                return True
        else:
            arg[1] = "x?"
            return True

    def disambiguation_nationality(self, triple, sent):
        '''
        属性"国籍"的消歧处理
        :param triple: 输入一个候选的三元组
        :param sent: 用户输入的问句
        :return: 返回结果为两个：一个是该三元组是否符合该三元组，
                 另一个是消歧过后的三元组信息
        '''
        # 排除subject词和object提取内容错误的情况，例如将属性值匹配到了subject和object槽位的情况
        if re.search(attributes_regex, triple['object']) or re.search(attributes_regex, triple['subject']):
            return [False, {}]
        # 排除subject词是一些无意义的表述的情况
        if re.search(general_pattern, triple['subject']):
            return [False, {}]
        replace_word = '属不'
        pattern_0 = '隶属|前身|影响'
        triple['subject'] = re.sub(replace_word, '', triple['subject'])
        # 排除一些相似属性的干扰
        if re.search(pattern_0, sent):
            return [False, {}]
        # 剔除国籍+人的情况，仅保留国籍信息
        if '人' in triple['object']:
            triple['object'] = triple['object'].replace('人', '')
        if triple['object'] != 'x?':
            # 通过字典树匹配的方式来确定提取的object是否在国籍字典里
            trie_result = self.trie_matcher.trie_match(triple['object'])
            if 'country' in trie_result:
                triple['object'] = trie_result['country'][0]
                return [True, triple]
        else:
            triple['object'] = 'x?'
            return [True, triple]

        def _normalize_nationality_args(self, arg, sent):
            arg[1] = self._normalize_arg(arg[1])
            return (self._normalize_arg(arg[0]), arg[1])

        def _check_birthPlace_arg(self, arg, sent):
            if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
                return False
            if re.search(general_pattern, arg[0]):
                return False
            replace_name = "是不|吗|么"
            sent = sent.replace("吗", "")
            pattern_1 = "哪族|国人"
            if re.search(pattern_1, sent):
                return False
            if "多少" == arg[0]:
                return False
            if arg[1] == "":
                return False
            if arg[1] == 'x?':
                return True
            else:
                arg[1] = arg[1].replace("吗","")
                #trie_result = self.trie_matcher.trie_match(arg[1])
                # if "city" in trie_result:
                #   for city in trie_result["city"]:
                #       if not city in arg[1]:
                #           arg[1] = arg[1] + city
                #if "city" in trie_result:
                #    arg[1] = trie_result['city'][0]
                return True
                #else:
                #    return False

    def _normalize_birthPlace_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _normalize_spouse_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_spouse_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_friend_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_friend_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if "好朋友" in sent and arg[0][-1] == "好":
            arg[0] = arg[0][:-1]
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人?|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'
        arg[1] = arg[1].replace('的', '')
        return True

    def _normalize_parent_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_parent_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'

        return True


    def _normalize_father_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_father_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'

        return True


    def _normalize_mother_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_mother_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'

        return True


    def _normalize_children_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_children_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_brother_sister_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_brother_sister_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        if re.search("谁|哪个人|哪一个人|哪些人?|什么人|哪个|哪个家伙|哪个美女|哪个帅哥|哪一个|哪位|哪几个|的名字|什么|哪人", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_alias_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_alias_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace('吗', '')
        arg[1] = arg[1].replace('叫', '')
        pattern_1 = "毕业学校|母校|毕业的学校|毕业院校|网站名称"
        if re.search(pattern_1, sent):
            return False
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|多大|多高|几号|几|何种|多细|怎样|几何|哪个|哪一个", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_ethnic_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_ethnic_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|多大|多高|几号|几|何种|多细|怎样|几何|哪个|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        if arg[1] == u'x?':
            return True
        else:
            if "族" in arg[1]:
                return True
            else:
                arg[1] = arg[1] + u'族'
                return True

    def _normalize_graduate_school_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_graduate_school_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        if arg[1] == "":
            arg[1] = "x?"
        arg[0] = arg[0].replace("大学", "")
        arg[0] = arg[0].replace("完成", "")
        pattern_2 = "完成|吗|在"
        arg[1] = re.sub(pattern_2, "", arg[1])
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|几|何种|多细|怎样|几何|哪个|哪一个|哪几个|哪种|哪一种|哪所|哪一所", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_education_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_education_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        pattern_0 = "毕业后|有没有|在学校"
        arg[0] = re.sub(pattern_0, "", arg[0])
        if arg[1] == "":
            arg[1] = 'x?'
        return True

    def _normalize_faith_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_faith_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace("吗", "")
        arg[1] = arg[1].replace("徒", "教")
        pattern_1 = "上帝"
        pattern_2 = "推崇|崇拜|信奉|崇奉|内心|心中"
        arg[0] = re.sub(pattern_2, "", arg[0])
        if arg[0][-1] == "所":
            arg[0] = arg[0][:-1]
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|几|何种|多细|怎样|几何|哪个|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        if re.search(pattern_1, arg[1]):
            arg[1] = "有神论"
        if "佛" in arg[1]:
            arg[1] = "佛教"
        if "耶稣" in arg[1]:
            arg[1] = "基督教"
        if "穆斯林" in arg[1]:
            arg[1] = "伊斯兰教"
        if arg[0][-1] == "相" and "相信" in sent:
            arg[0] = arg[0][:-1]
        return True

    def _normalize_nativePlace_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_nativePlace_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace("吗", "")
        arg[1] = arg[1].replace("在", "")
        arg[1] = arg[1].replace("的", "")
        if re.search("哪里|哪儿|什么地方|哪|哪个地方|什么|啥", arg[1]):
            arg[1] = u'x?'
        return True

    def _normalize_position_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_position_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = arg[1].replace("吗", "")
        arg[1] = arg[1].replace("一职", "")
        pattern_0 = u'最近|需要|主要|在篮球队'
        if arg[1] == "":
            arg[1] = "x?"
        arg[0] = re.sub(pattern_0, "", arg[0])
        if re.search("职务|官职", arg[0]) or re.search("职务|官职", arg[1]):
            return False
        if re.search("什么|啥|嘛|多少|什么类型|什么类别|什么样|怎么样|几|何种|多细|怎样|几何|哪个|哪些|哪一个|哪几个|哪种|哪一种", arg[1]):
            arg[1] = u'x?'
        pattern_3 = u'荣誉|荣耀|荣誉奖|成立|建立|创办|上市|类型|出版|版本|版|版次|企业开发|物业|翻译'
        if re.search(pattern_3, sent):
            return False
        if arg[1] == u'x?':
            return True

        trie_result = self.trie_matcher.trie_match(arg[1])
        if "position" in trie_result:
            arg[1] = trie_result['position'][0]
            return True
        else:
            return False

    def _normalize_BWH_args(self, arg, sent):
        arg[1] = self._normalize_arg(arg[1])
        return (self._normalize_arg(arg[0]), arg[1])

    def _check_BWH_arg(self, arg, sent):
        if re.search(attributes_regex, arg[1]) or re.search(attributes_regex, arg[0]):
            return False
        if re.search(general_pattern, arg[0]):
            return False
        arg[1] = cn2dig(arg[1])
        pattern_1 = "(\\d+)到(\\d+)"
        regex_1 = re.search(pattern_1, arg[1])
        if regex_1:
            number_1 = regex_1.group(1)
            number_2 = regex_1.group(2)
            arg[1] = str(number_1) + '-' + str(number_2)
        elif ("大于" in arg[1] or "超过" in arg[1]):
            if "不" in arg[1] or "没" in arg[1]:
                number = re.search(u'\\d+', arg[1]).group(0)
                arg[1] = '-' + str(number)
            else:
                number = re.search(u'\\d+', arg[1]).group(0)
                arg[1] = str(number) + '-'
        elif ("小于" in arg[1] or "低于" in arg[1]):
            if "不" in arg[1] or "没" in arg[1]:
                number = re.search(u'\\d+', arg[1]).group(0)
                arg[1] = str(number) + '-'
            else:
                number = re.search(u'\\d+', arg[1]).group(0)
                arg[1] = '-' + str(number)
        return True


argsDisambiguation = ArgsDisambiguation()
