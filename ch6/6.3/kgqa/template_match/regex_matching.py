#!/usr/bin/env python
# -*- coding:utf8 -*-

__author__ = 'winnie'

import re
# from read_config import config
from util.tools import util
from template_match.reg_util import *
from util.trie_match import entity_trie
from util.trie_match import property_trie
# from data_access.kg_service import kg_search
template_path = './data/'#config.template_path  #/data/regex/question_template/
template_variable_path = './data/'#config.template_variable_path #/data/regex/
# print(os.pwd())

class RegexMatching:
    def __init__(self):
        """
        构造问答匹配器
        目前所有正则模板通用一套变量文件：regex_variable中配置
        第一层模板：general_template_file
        第二层模板：template_file_list
        两层模板共享regex_variable变量文件
        """
        # 正则模板文件列表，变量文件
        self.special_question_template_file = 'special_question_template.json'
        self.complex_question_template_file = 'complex_question_template.json'
        self.general_yes_no_question_template_file = 'general_yes_no_question_template.json'
        self.property_template = 'person_property_template.json'
        self.regex_variable_file = 'regex_variables.json'
        self.regex_variable = util.read_json(template_variable_path + self.regex_variable_file)
        self.regex_variable_dict = {} #与regex_variable的区别在于该字典中的变量对应的值都是正则编译过的，而非含变量名称的值
        # 第一层特殊疑问句通用模板集
        self.regex_template_special = self.build_regexes(self.regex_variable, template_path + self.special_question_template_file)
        # 第二层一般疑问句通用模板集
        self.regex_template_complex = self.build_regexes(self.regex_variable, template_path + self.complex_question_template_file)
        self.regex_template_yes_no = self.build_regexes(self.regex_variable, template_path + self.general_yes_no_question_template_file)
        self.regex_dict_property = self.build_regexes(self.regex_variable, template_path + self.property_template)#self._regex_dict_merge()

    def build_regexes(self, regex_var, regex_path):
        """
        加载模板正则表达式中的变量，将其与模板组装起来形成一个完整正则表达式，并编译正则
        :param var_path: 模板变量文件的路径
        :param regex_path: 模板库文件的路径
        :return: 字典数据结构，其中包含加载了正则变量编译后的正则，供后续匹配使用
        """
        for key in regex_var['basic']:
            # 将basic变量的value存放在对应的regex_variable_dict当中
            self.regex_variable_dict[key] = regex_var['basic'][key]

        for key in (regex_var['combo']):
            # 找出combo变量中用到的basic变量
            mm = re.findall("\{([^\d]+?)\}", regex_var['combo'][key])
            # 将combo匹配到的变量对应的变量值替换到combo变量中
            used_vars = {var: self.regex_variable_dict[var] for var in set(mm)}
            val = regex_var['combo'][key].format(**used_vars)
            self.regex_variable_dict[key] = val

        # 读取模板库中的全部模板配置
        regex_dict = util.read_json(regex_path)
        for rel in regex_dict:
            for regex in regex_dict[rel]["regex"]:
                regex_expr = regex[0]
                # 找出正则模板中用到的全部变量
                mm = re.findall("\{([^\d]+?)\}", regex_expr)
                if mm:
                    # 对匹配到的变量去重，形成替换映射字典
                    used_vars = {var: self.regex_variable_dict[var] for var in set(mm)}
                    # 将变量组装到正则模板中
                    reg = regex_expr.format(**used_vars)
                else:  # mm == []，针对以前不含有变量的正则表达式
                    reg = regex_expr
                regex.append(re.compile(reg)) # 编译正则表达式并append到list中

        return regex_dict

    def _merge_dicts(self, dicts):
        """
        合并多个字典并返回合并的字典
        :param dicts: 需要合并的多个字典
        :return: 合并后的字典
        """
        result = {}
        for d in dicts:
            result.update(d)
        return result

    # 仅在合并多个变量文件时使用到，平时用不到
    def merge_variables(self,dicts):
        '''
        合并多个正则变量文件
        :param dicts: 需要合并的多个变量字典
        :return: 合并后的正则字典
        '''
        result = {}
        for d in dicts:
            for key in d:
                if key not in result:
                    result[key] = d[key]
                else:
                    # 合并每一大类变量中的每个变量的值
                    type_res_dict = result[key]
                    type_new_dict = d[key]
                    for var in type_new_dict:
                        # 新变量添加
                        if var not in type_res_dict:
                            #print 'not in',var
                            type_res_dict[var] = type_new_dict[var]
                        # 已有变量有修改
                        elif type_res_dict[var] != type_new_dict[var]:
                            #print 'diff ',var
                            res_value_list = type_res_dict[var].split('|')
                            new_value_list = type_new_dict[var].split('|')
                            union_list = self._union_list_order(res_value_list,new_value_list)
                            type_res_dict[var] = '|'.join(union_list)

        # 这段将字典里字段的编码全部转为utf8，方便以utf8格式以json格式写入文件
        ret_dict = {}
        for key in result:
            value_dict = result[key]
            new_var_dict = {}
            for var in value_dict:
                new_var_dict[var.encode('utf8')] = value_dict[var].encode('utf8')
            ret_dict[key.encode('utf8')] = new_var_dict

        return ret_dict

    def _union_list_order(self, l1, l2):
        '''
        求两个list的并集，l1中没有，l2中有的元素，追加到l1后面
        :return: 求并集
        '''
        for e in l2:
            if e not in l1:
                l1.append(e)
        return l1

    def deal_back_object(self, object_string):
        """
        后处理一般疑问句模板的object
        :param object_string:
        :return:
        """

        #male
        regex_male = re.search(reg_male, object_string)
        if regex_male:
            match_pattern = regex_male.group()
            if match_pattern == object_string:
                object_string = "male"

        #female
        regex_female = re.search(reg_female, object_string)
        if regex_female:
            match_pattern = regex_female.group()
            if match_pattern == object_string:
                object_string = "female"

        return object_string

    def _extract_args(self, regex, match):
        '''
        把 一条regex中，匹配到的部分的arg1和arg2提取出来
        :param regex: 一条正则表达式
        :param match: 匹配到的子串
        :return: 匹配到的arg1和arg2的内容，以及他们对应的span
        '''
        if regex[1] == "n/a":
            arg1 =  "你" if match.group('arg1') == None else match.group('arg1')
            arg1_span = match.span('arg1')
        else: 
            arg1 = regex[1] #user
            arg1_span = (-1, -1)

        if regex[2] == "n/a": #说明是从原句中抽取的object
            arg2 = match.group('arg2') #arg2函数
            arg2_span = match.span('arg2')
        else:
            arg2 = regex[2]
            arg2_span = (-1, -1)
        return [arg1, arg1_span, arg2, arg2_span, regex[3]]

    def _slots_filter(self, slots_dict):
        ret = {}
        for key in slots_dict:
            if slots_dict[key]:
                ret[key] = slots_dict[key]
        return ret

    def max_len_match(self, match_str, match_results):
        '''
        将问句中匹配到的子串与外部资源库如实体库、属性库、关系库匹配结果进行比较
        选择最大长度的匹配结果作为最优选择
        :param match_str: 问句中匹配的子串
        :param match_list: 外部资源库中匹配到的结果
        :return: 返回校验过后的匹配结果
        '''
        max_len = 0
        max_len_str = ''
        for match in match_results:
            if match in match_str:
                if max_len < len(match):
                    max_len = len(match)
                    max_len_str = match
        if max_len_str == '':
            max_len_str = match_str
        return max_len_str


    def deal_candi_cell(self, slots_dict, template_type, sent):
        candi = {}
        candi['subject'] = slots_dict['subject']
        matched_dict_subject = entity_trie.trie_match(candi['subject'])
        candi['subject'] = self.max_len_match(candi['subject'], matched_dict_subject)
        # matched_dict_predicate = entity_trie.trie_match(slots_dict['predicate'])
        # slots_dict['predicate'] = self.max_len_match(slots_dict['predicate'], matched_dict_predicate)

        if template_type == "general_regex":
            slots_dict['predicate'] = slots_dict['predicate'].replace("吗", "")
            slots_dict['predicate'] = slots_dict['predicate'].replace("的", "")
            matched_dict_predicate = property_trie.trie_match(slots_dict['predicate'])
            if slots_dict['subject'] in matched_dict_subject and slots_dict['predicate'] in matched_dict_predicate:
                candi['predicate'] = slots_dict['predicate']
                candi['subject'] = slots_dict['subject']
                return candi
            else:
                return []

        if template_type == "how_many":
            if "人数" not in slots_dict['predicate'] and "数量" not in slots_dict['predicate']:
                candi['predicate'] = slots_dict['predicate'] + "数量"
                return candi

        if template_type == "where":
            slots_dict['predicate'] = slots_dict['predicate'].replace("的", '')
            if "生" in slots_dict['predicate']:
                slots_dict["predicate"] = "出生地"
            if "人" in slots_dict['predicate']:
                if "国" in slots_dict['predicate']:
                    slots_dict["predicate"] = "国籍"
                else:
                    slots_dict["predicate"] = "出生地"
            if "地点" not in slots_dict['predicate'] and "地点" in sent:
                slots_dict["predicate"] = slots_dict["predicate"] + "地点"
            else:
                slots_dict['predicate'] = slots_dict['predicate'] + "地点"

        if template_type == "how":
            if "长" in slots_dict['predicate']:
                slots_dict['predicate'] = "长度"
            # if "大" in slots_dict['predicate']:
            #     slots_dict_cand = ["面积", "年龄"]
            #     for cand in slots_dict_cand:
            #         if kg_search(candi['subject'], cand, "x?"):
            #             slots_dict['predicate'] = cand
            #             break
            if "高" in slots_dict['predicate']:
                slots_dict['predicate'] = "高度"

        if template_type == "what":
            if "东西" in slots_dict['predicate']:
                slots_dict['predicate'] = ""
            if "省" in slots_dict['predicate'] or "市" in slots_dict['predicate'] or "县" in slots_dict['predicate'] or "区" in slots_dict['predicate']:
                slots_dict['predicate'] = "地点"

        if template_type == "when":
            if "死" in slots_dict['predicate']:
                slots_dict['predicate'] = "去世"
            if "时间" not in slots_dict['predicate'] and "时代" not in slots_dict['predicate'] and "时候" not in \
                    slots_dict['predicate']:
                slots_dict['predicate'] = slots_dict['predicate'].replace("的", '')
                if slots_dict['predicate'] == "处于":
                    slots_dict['predicate'] = "所处"
                if "时间" in sent:
                    slots_dict['predicate'] = slots_dict['predicate'] + "时间"
                elif ("时代" in sent) or ("朝代" in sent):
                    slots_dict['predicate'] = slots_dict['predicate'] + "时代"
                elif ("年代" in sent):
                    slots_dict['predicate'] = slots_dict['predicate'] + "年代"
                elif "生日" in sent:
                    slots_dict['predicate'] = slots_dict['predicate']
                else:
                    slots_dict['predicate'] = slots_dict['predicate'] + "时间"

        if template_type == "which":
            if "类别" in sent:
                if "类别" not in slots_dict['predicate']:
                    slots_dict['predicate'] = slots_dict['predicate'] + "类别"
            elif ("类型" in sent):
                if "类型" not in slots_dict['predicate']:
                    slots_dict['predicate'] = slots_dict['predicate'] + "类型"
            elif ("区" == slots_dict['predicate']):
                slots_dict['predicate'] = "地区"
            elif ("公司" in sent or "企业" in sent):
                if "公司" not in slots_dict['predicate'] and "公司" in sent:
                    slots_dict['predicate'] = slots_dict['predicate'] + "公司"
                elif ("企业" not in slots_dict['predicate'] and "企业" in sent):
                    slots_dict['predicate'] = slots_dict['predicate'] + "企业"

        if template_type == "who":
            if slots_dict['predicate'] == "写":
                slots_dict['predicate'] = "作者"
            elif "唱" in slots_dict['predicate']:
                slots_dict['predicate'] = "歌曲原唱"
            elif "提出" in slots_dict['predicate']:
                slots_dict['predicate'] = "提出"
            elif (slots_dict['predicate']) == "演":
                slots_dict['predicate'] = "演员"
            # elif "朝" in slots_dict['subject'] and re.search(slots_dict['predicate'], "创立|开创|建立|创建"):
            #     slots_dict_cand = ["开创者", "建立者", "开国皇帝", "开国君主"]
            #     for cand in slots_dict_cand:
            #         if kg_search(candi['subject'], cand, "x?"):
            #             slots_dict['predicate'] = cand
            #             break
            elif ("人" not in slots_dict['predicate'] and "者" not in slots_dict['predicate'] and re.search(slots_dict['predicate'], reg_verb)):
                slots_dict['predicate'] = slots_dict['predicate'] + "人"
            else:
                slots_dict['predicate'] = slots_dict['predicate']

        if "隶属" in sent:
            slots_dict['predicate'] = "隶属"
        candi['predicate'] = slots_dict.get('predicate', '')
        if candi['predicate'] == "":
            if template_type == "where_special":
                candi['predicate'] = '地点'
                if slots_dict['subject'] in matched_dict_subject:
                    candi['subject'] = slots_dict['subject']
                    return candi
                else:
                    return []
            elif (template_type == "abstract"):
                if "为什么" not in sent:
                    candi['predicate'] = 'abstract'
                    if slots_dict['subject'] in matched_dict_subject:
                        candi['subject'] = slots_dict['subject']
                        return candi
                    else:
                        return []
        #if candi['predicate'] != "x?":
        matched_dict_predicate = property_trie.trie_match(candi["predicate"])
        candi['predicate'] = self.max_len_match(candi['predicate'], matched_dict_predicate)
        if template_type == "where" and candi['predicate'] == "地点" and len(matched_dict_predicate) >= 2:
            candi['predicate'] = slots_dict['predicate'].replace("地点", "")
        return candi

    def get_general_candidates(self, sent=""):
        '''
        第一层获得候选，逻辑与之前的完全不同，需要通过trie树匹配根据变量名称，确定到底是哪个意图，以前是根据正则属于哪个属性的，就直接获得意图
        :param sent: 传入的句子
        :return:
        '''
        candidates_list = []
        for template_type in self.regex_template_special:
            for regex in self.regex_template_special[template_type]['regex']:
                m = regex[2].search(sent)
                if m:
                    slots_dict = m.groupdict()
                    subject = slots_dict['subject']
                    pattern_1 = "(.+)(的)(.+)"
                    if re.search(pattern_1, subject):
                        break
                    if template_type != "when" and ("时间" in sent or "日期" in sent or "时代" in sent or "时候" in sent or "年代" in sent or "朝代" in sent):
                        break
                    if (template_type != "where" and template_type != "where_special") and ("地址" in sent or "地点" in sent or "位置" in sent or "产地" in sent or "方向" in sent or "地方" in sent):
                        break
                    if template_type != "which" and ("类型" in sent ):
                        break

                    candi = self.deal_candi_cell(slots_dict, template_type, sent)
                    if not candi or candi["predicate"] == "":
                        break
                    candi['object'] = "x?"
                    if template_type =="how_many" or template_type == "where_special":
                        return [candi]
                    else:
                        candidates_list.append(candi)
        return candidates_list

    def get_candidates_for_complex_question(self, sent):
        '''
        匹配复杂类问句模板，获得候选答案的三元组信息
        '''
        candidates_list = []
        for template_type in self.regex_template_complex:
            for regex in self.regex_template_complex[template_type]['regex']:
                m = regex[2].search(sent)
                if m:
                    slots_dict = m.groupdict()
                    candi = {}
                    # 处理subject，并进行实体库校验
                    candi['subject'] = slots_dict['subject']
                    matched_subject = entity_trie.trie_match(candi['subject'])
                    candi['subject'] = self.max_len_match(candi['subject'], matched_subject)
                    # 处理比较类问题的object
                    if template_type == "compare_qa":
                        candi['object'] = slots_dict['object']
                        matched_object = entity_trie.trie_match(candi['object'])
                        candi['object'] = self.max_len_match(candi['object'], matched_object)
                        # 虽然存放在object槽位，但是会加上比较类主体的标识
                        candi['object'] = "subject_compare:" + candi['object']
                    # 处理多跳查询类问题的object
                    if template_type == "jump_qa":
                        candi['object'] = slots_dict['object']
                        matched_object = property_trie.trie_match(candi['object'])
                        if matched_object !=[]:
                            candi['object'] = self.max_len_match(candi['object'], matched_object)
                        # 虽然存放在object槽位，但是会加上多跳主体的标识
                        candi['object'] = "subject_jump:" + candi['object']
                    # 处理谓语predicate
                    candi['predicate'] = slots_dict['predicate']
                    # 针对一些特殊的表述进行predicate标准化
                    if '哪里人' in slots_dict['predicate']:
                        candi['predicate'] = '出生地'
                    if '长' in slots_dict['predicate']:
                        candi['predicate'] = '长度'
                    matched_predicate = property_trie.trie_match(candi['predicate'])
                    candi['predicate'] = self.max_len_match(candi['predicate'], matched_predicate)

                    candidates_list.append(candi)
        return candidates_list

    def get_candidates_for_yes_no_question(self, sent):
        '''
        匹配一般疑问句模板，获得候选三元组信息
        :param sent: 用户输入的问句
        :return: 候选三元组的list
        '''
        triple_candidates = []
        for template_type in self.regex_template_yes_no:
            for regex in self.regex_template_yes_no[template_type]['regex']:
                # regex的构成[原始配置模板, 例句, 加载变量后编译后的正则]
                m = regex[2].search(sent)
                if m: # 如果匹配到结果
                    matched_slots = m.groupdict() # 取出对应槽位的值
                    candi = {}
                    candi['subject'] = matched_slots['subject']
                    # 实体校验：基于图谱中全部实体词构建的trie树结构匹配提取出的subject子串内容是否是一个实体
                    matched_subject = entity_trie.trie_match(candi['subject'])
                    candi['subject'] = self.max_len_match(candi['subject'], matched_subject)
                    candi['predicate'] = matched_slots['predicate']
                    # 属性校验：基于图谱中全部属性构建的trie树结构匹配提取出的predicate子串内容是否是一个属性值
                    matched_predicate = property_trie.trie_match(candi['predicate'])
                    candi['predicate'] = self.max_len_match(candi['predicate'], matched_predicate)
                    candi['object'] = matched_slots['object']
                    # 去掉结尾的无关紧要的语气词和标点
                    ignore_end = ['呀','吗','的','?','？','嘛']
                    if candi['object'][-1] in ignore_end:
                        candi['object'] = candi['object'][:-1]
                    triple_candidates.append(candi)
        return triple_candidates


    def get_rel_candidates(self, sent=""):
        """
        第二层获得候选
        用加载完变量后的全部正则表达式，去匹配句子
        :param sent: 正则去匹配的句子
        :return: candidates, 候选关系列表，包括0个、1个或多个关系元组。每个关系元组包含的信息见下面代码中注释
        """
        # candidates = []
        candidates_list = []
        for rel in self.regex_dict_property: #编译后的正则表达式
            for regex in self.regex_dict_property[rel]["regex"]:
                match = regex[4].search(sent) # 这里regex[3]是编译过的正则
                if match:
                    # print('match', match)
                    # 如果匹配到一条正则，提取arg1和arg2和arg3
                    arg1, arg1_span, arg2, arg2_span, arg3 = self._extract_args(regex, match)
                    candi={}
                    candi['rel'] = rel # 意图
                    candi['reg_original'] = regex[0] # 匹配的原始正则
                    candi['reg_load_variable'] = regex[4].pattern
                    candi['sent_matched'] = match.group(0)
                    candi['extract_arg1'] = arg1
                    candi['extract_arg1_span'] = arg1_span
                    candi['extract_arg2'] = arg2
                    candi['extract_arg2_span'] = arg2_span
                    candi['extract_arg3'] = arg3
                    candidates_list.append(candi)
                    # candidates.append(
                    #     # 关系元组格式 [关系，加载变量前的正则，加载变量后的正则，正则匹配到的句子部分，正则匹配出的arg1, arg1在sent中的位置，正则匹配出的arg2，arg2在sent中的位置]
                    #     # note: 因为会做归一，所以arg1_span和arg2_span这两个位置信息会变得无用。它们只表达从句子中抠取出来的arg1和arg2在句子中的位置
                    #     [rel, regex[0], regex[3].pattern, match.group(0), arg1, arg1_span, arg2, arg2_span])
                    # break  # 如果某个关系中的某条正则命中，则跳过这个关系中余下没扫描的正则

        return candidates_list#candidates

regex_matcher = RegexMatching()
