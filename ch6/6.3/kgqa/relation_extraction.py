#!/usr/bin/env python
# -*- coding:utf-8 -*-


import re
from util.tools import util
from util.trie_match import entity_trie
from util.trie_match import property_trie
# from data_access import kg_service
from template_match.reg_util import *
from template_match.regex_matching import regex_matcher
from template_match.args_disambiguation import argsDisambiguation



class RelationExtractor:
    '''
    实现答案查询三元组的抽取
    需要其他两个.py文件的支持：
    · regex_generation.py 用于将带变量的正则模板中的变量替换生成可以匹配的正则表达式
    · args_disambiguation.py 主要实现多个正则冲突时的归一消歧逻辑
    '''
    def __init__(self):
        self.args_disambiguation = argsDisambiguation  # 关系抽取arg1, arg2处理器
        # self.args_disambiguation_economic = argsDisambiguation_economic
        # self.args_disambiguation_history = argsDisambiguation_history
        # self.args_disambiguation_social = argsDisambiguation_social
        # self.args_disambiguation_art = argsDisambiguation_art
        # self.args_disambiguation_PE = argsDisambiguation_PE
        # self.args_disambiguation_science = argsDisambiguation_science
        # self.args_disambiguation_natural = argsDisambiguation_natural
        # self.args_disambiguation_culture = argsDisambiguation_culture
        # self.args_disambiguation_geography = argsDisambiguation_geography
        # self.args_disambiguation_life = argsDisambiguation_life
        self.attributes_dict = attributes_dict
        self.regex_matcher = regex_matcher  # rel_matcher  # 关系匹配器
        self.attributes_rever_dict = {}
        for key in self.attributes_dict:
            self.attributes_rever_dict[self.attributes_dict[key]] = key

    def candidates_disambiguation(self, triple_candidates, sent):
        """
        对关系列表中的多个候选关系进行归一和消歧。
        :param rel_candidates: 要进行归一和消歧的候选关系列表
        :param sent: 输入语句
        :return: 完成了归一和消歧的候选关系列表，可能包含0个，1个或多个归一和消歧后的候选关系
        """
        triple_candidates_sorted = []
        print('!!!candidates and disambiguation:',triple_candidates)
        for triple in triple_candidates:
            # compatibility：存放是否兼容，True or False
            # normalized_args：标准化的[arg1, arg2]
            compatibility_person, normalized_args_person = self.args_disambiguation.check_args_compatibility(triple, sent)

            all_compatibility = [compatibility_person]#, compatibility_ecomomic, compatibility_history, compatibility_social, compatibility_art, compatibility_PE, compatibility_science, compatibility_natural, compatibility_culture, compatibility_geography, compatibility_life]
            all_normalized_args = [normalized_args_person]#, normalized_args_economic, normalized_args_history, normalized_args_social, normalized_args_art, normalized_args_PE, normalized_args_science, normalized_args_natural, normalized_args_culture, normalized_args_geography,normalized_args_life]

            # print('###'*90)
            # 整理成输出格式
            for compatibility, normalized_args in zip(all_compatibility, all_normalized_args):
                if compatibility:  # 如果兼容
                    triple['normalized_args'] = normalized_args
                    extract_arg2 = triple['extract_arg2']
                    norm_arg2 = triple['normalized_args'][1]
                    match_sentence = triple['sent_matched']
                    # TODO: remove the following assertions when the code is stable
                    # assert isinstance(extract_arg2, unicode)
                    #assert isinstance(norm_arg2, unicode)
                    # assert isinstance(match_sentence, unicode)
                    # assert isinstance(sent, unicode)
                    # ranking策略
                    norm_arg2 = str(norm_arg2)
                    if extract_arg2 == "":
                        extract_arg2 = "1"
                    match_score = float(len(match_sentence)) / len(sent)
                                  # * 0.6 + float(len(norm_arg2)) / len(extract_arg2) * 0.4  # TODO: 注意这里的权重设置
                    triple['match_score'] = match_score
                    triple['attribute_index'] = int(attributes_order.get(triple['rel'], '1'))
                    triple_candidates_sorted.append(triple)
        if len(triple_candidates_sorted) > 1:  # 如果有多个兼容的候选关系，则按match_score从大到小排序
            triple_candidates_sorted.sort(key=lambda e: e['match_score'], reverse=True)
            # triple_candidates_sorted.sort(key=lambda e: e['attribute_index'])
        if triple_candidates_sorted:
            triple_candidates_sorted = [triple_candidates_sorted[0]]
        return triple_candidates_sorted


    # def triple_extract_general(self, sent):
    #     '''
    #     第一层，特殊疑问句通用模板层
    #     :param sent: 输入语句
    #     :return:
    #     '''
    #     general_candidates = self.regex_matcher.get_general_candidates(sent)
    #     return general_candidates, general_candidates

    # def triple_extract_complex_qa_question(self, sent):
    #
    #     '''
    #     抽取一般
    #     :param sent:
    #     :return:
    #     '''
    #     general_candidates = self.regex_matcher.get_general_candidates_for_complex_qa_question(sent)
    #     return general_candidates, general_candidates

    # def triple_extract_general_for_general_question(self, sent):
    #     general_candidates = self.regex_matcher.get_general_candidates_for_general_question(sent)
    #     return general_candidates, general_candidates
    
    def max_len_match(self, match_str, match_list):

        max_len = 0
        max_len_str = ''
        for match_cell in match_list:
            if match_cell in match_str:
                if max_len < len(match_cell):
                    max_len = len(match_cell)
                    max_len_str = match_cell
        if max_len_str == "":
            max_len_str = match_str
        return max_len_str

    # def select_triple_list(self, triple_list):
    #     triple_list_new = []
    #     if len(triple_list) != 0:
    #         for triple in triple_list:
    #             kg_res = kg_service.search_object_service_fuzzy(triple['subject'], triple['predicate'], triple['object'])
    #             if len(kg_res) != 0:
    #                 triple_list_new = [triple, kg_res]
    #                 break
    #     if len(triple_list_new) == 0:
    #         triple_list_new = [triple_list[0], []]
    #     return triple_list_new

    def delete_duplicate(self, dict):
        temp_list = list(set([str(i) for i in dict]))
        dict = [eval(i) for i in temp_list]
        return dict

    def sent_preprocess(self, sent):
        '''
        去除问句中的无关描述，将一些含糊表述标准化
        :param sent: 输入问句
        :return: 返回处理过后的句子
        '''
        remove_word_prefix = "(我想|你|我|可以|请|是否|是否能|应该|能){0,}(知道|猜猜|回答|告诉|问下?|难道|清楚|说下|猜)(一猜)?(我|看){0,}"
        replace_word = "在公司|对吗"
        is_name = "(是不是|到底是不是|是否为|才是|有可能是|不是|不是为|分别是)(叫作|叫做)?"
        have_name = "共有|才有|总共有"
        shuyu_name = "属不属于|是否属于"
        include_name = "是否包括|包不包括|是否含"
        sent = re.sub(is_name,"是",sent)
        sent = re.sub(have_name,"有",sent)
        sent = re.sub(shuyu_name, "属于", sent)
        sent = re.sub(remove_word_prefix,"",sent)
        sent = re.sub(include_name, "包括", sent)
        sent = re.sub(replace_word,"",sent)
        sent = util.remove_punctuation(sent)
        return sent

    def triple_extract(self, sent):
        '''
        分两层调用模板，
        第一层，通用模板层
        处理逻辑：加载通用句式模板，根据槽位抠出一定的内容，进行标准化处理，
        第二层，详细模板层
        处理逻辑：加载各个属性包含的正则模板，然后对能匹配上的多个模板进行消歧和排序处理，得到最终的候选三元组
        :param sent: 输入语句
        :return:
        '''
        # 问句前处理
        sent = self.sent_preprocess(sent)
        # 解析开始
        # triple_list, _ = self.triple_extract_complex_qa_question(sent)
        triple_list = self.regex_matcher.get_candidates_for_complex_question(sent)
        # print('triple_list',triple_list)
        if triple_list:
            triple_list = [triple_list[0],[]]#self.select_triple_list(triple_list)  # [triple_list[0]]
        # print 1, triple_list[0]['subject'], triple_list[0]['predicate']
        if (not triple_list) or (triple_list[0]['subject'] == "x?") or (triple_list[0]['predicate'] == "x?"):
            triple_list = self.regex_matcher.get_general_candidates(sent)#self.triple_extract_general(sent)
            if triple_list:
                triple_list = self.delete_duplicate(triple_list)
                triple_list_new = triple_list
                for triple in triple_list:
                    matched_dict_subject = entity_trie.trie_match(triple['subject'])
                    matched_dict_predicate = property_trie.trie_match(triple['subject'])
                    new_matched_dict_subject = []
                    for cell_subject in matched_dict_subject:
                        if cell_subject not in matched_dict_predicate:
                            new_matched_dict_subject.append(cell_subject)
                    # print('new_matched_dict_subject',new_matched_dict_subject)
                    triple['subject'] = self.max_len_match(triple['subject'], new_matched_dict_subject)
                    triple_list_new = [triple_list[0],[]]#self.select_triple_list(triple_list)  # self.select_triple_list(triple_list)  # [triple_list[0]]
                    if len(triple_list_new[1]) != 0:
                        break
                triple_list = triple_list_new

            if (not triple_list):
                print('Template Level 3')
                relation_candidates = self.regex_matcher.get_rel_candidates(sent)# 生成候选关系列表//
                # print('relation_candidates',relation_candidates)
                candidates_sorted = self.candidates_disambiguation(relation_candidates, sent)  # 获取归一、消歧、排序后的关系列表
                triple_list = []
                for candidate in candidates_sorted:
                    triple = {}
                    arg1 = candidate['normalized_args'][0]
                    if arg1 != u'':
                        if arg1[-1] in ["是", "滴", "的"]:
                            arg1 = arg1[:-1]
                        triple['subject'] = arg1
                        regex_1 = u'(.+)(的)(.+)'
                        if re.search(regex_1, arg1):
                            break
                        matched_dict_subject = entity_trie.trie_match(arg1)
                        matched_dict_predicate = property_trie.trie_match(arg1)
                        new_matched_dict_subject = []
                        for cell_subject in matched_dict_subject:
                            if cell_subject not in matched_dict_predicate:
                                new_matched_dict_subject.append(cell_subject)
                        if len(new_matched_dict_subject) == 0:
                            new_matched_dict_subject = matched_dict_subject
                        triple['subject'] = self.max_len_match(arg1, new_matched_dict_subject)
                        triple['predicate'] = candidate['rel']
                        triple['object'] = str(candidate['normalized_args'][1]).strip()
                        triple_list.append(triple)

                if not(triple_list):
                    triple_list = self.regex_matcher.get_candidates_for_yes_no_question(sent) #self.triple_extract_general_for_general_question(sent)
                    # triple_list = self.select_triple_list(triple_list)
                triple_list_new = triple_list

                for triple in triple_list:
                    if triple['predicate'] in self.attributes_rever_dict:
                        triple['predicate'] = self.attributes_rever_dict[triple['predicate']]
                    if 'object' in triple:
                        triple['object'] = triple['object']
                    else:
                        triple['object'] = "x?"
                    if len(triple['predicate']) == 1:
                        triple['predicate'] = None

                    triple_list_new = [triple_list[0],[]]#self.select_triple_list(triple_list)
                    if len(triple_list_new[1]) != 0:
                        break
                triple_list = triple_list_new
            # else:
            #     print('Template Level 2')
            #     matched_dict_subject = entity_trie.trie_match(triple_list[0]['subject'])
            #     matched_dict_predicate = property_trie.trie_match(triple_list[0]['subject'])
            #     new_matched_dict_subject = []
            #     for cell_subject in matched_dict_subject:
            #         if cell_subject not in matched_dict_predicate:
            #             new_matched_dict_subject.append(cell_subject)
            #     triple_list[0]['subject'] = self.max_len_match(triple_list[0]['subject'], new_matched_dict_subject)
        return triple_list#, candidates_sorted



relation_extractor = RelationExtractor()

