#!/usr/bin/env python
# -*- coding:utf8 -*-

import  configparser
# import synonyms
import json
import random
import re
import sys
import requests
from relation_template.reg_util import *
from data_access.kg_dao import kg_dao, schema_dao
# from data_access.kg_dao import acgn_kg_dao as kg_dao, schema_dao


# from util.word_embedding import get_similarity
# reload(sys)
# sys.setdefaultencoding('utf-8')

__cf = configparser.ConfigParser()
__cf.read("./config.ini")
similarity_threshold = 0.8

def get_similarities(phrase):
    return phrase

def kg_search_o_by_sp(subject_id, predicate):
    '''
    根据subject_id和predicate查询object
    :param subject_id: subject结点
    :param predicate: 属性or关系
    :return: 返回subject在predicate属性下对应的值
    '''
    value = kg_dao.search_spo(subject_id, predicate)
    if not value:
        # 当无法匹配时，获取predicate的相似表述再进行查询
        predicate_similarities = get_similarities(predicate)
        for sim_pred in predicate_similarities:
            value = kg_dao.search_spo(subject_id, sim_pred)
            if value:
                return value
    if not value:
        return None
    return value


def kg_check_o_by_sp(subject_id, predicate, object):
    '''
    将实体链接后的三元组查询KG进行校验
    :param subject_id: subject结点的id
    :param predicate: 属性or关系
    :param object_id: predicate的值
    :return: 返回校验结果True or False
    '''
    value = kg_dao.search_spo(subject_id, predicate)
    if value:
        # 若能匹配成功，返回True
        if value in object or object in value:
            return True
    # 当无法匹配时，获取predicate的相似表述再进行查询
    predicate_similarities = get_similarities(predicate)
    for sim_pred in predicate_similarities:
        value = kg_dao.search_spo(subject_id, sim_pred)
        if value:
            # object校验的策略
            if value in object or object in value:
                return True
    return False




def kg_check_jump_qa(subject_id, predicate, object):
    '''
    复杂问题利用多跳查询进行三元组校验
    :param subject_id: subject结点的id
    :param predicate: 属性or关系
    :param object: 多跳信息值
    :return: 返回校验或查询结果
    '''
    # 当存在subject_jump时，属于一个二跳查询问题
    if object.startswith('subject_jump'):
        first_predicate = object.split(':', 1)[1]
        # 通过neo4j关系查询获取第二个三元组的subject的id
        second_subject_id = kg_dao.get_node_relation(subject_id, first_predicate)
        if second_subject_id:
            value = kg_dao.search_spo(second_subject_id, predicate)
            if value:
                # object校验的策略
                if value in object or object in value:
                    return True
    else: # 当非多跳查询问题时，执行传统的单spo三元组查询方法
        if object != 'x?':
            return kg_check_o_by_sp(subject_id, predicate, object)
        else:
            return kg_search_o_by_sp(subject_id, predicate)
    return False





def kg_search(subject, predicate, object):
    rst_list = []
    kg_search_rst = kg_dao.search_node_info_by_name(subject)
    for entity_info_list in kg_search_rst:
        # if predicate == 'abstract':
        #     ans = get_abstract(entity_info_list, 50)
        #     if ans:
        #         rst_list.append({'candidate_list': [ans], 'disambiguation': ''})
        #     return rst_list

        candidate_list = []
        hit_property_name = ''
        # direct and schema
        for entity_info_tuple in entity_info_list:
            property_name = entity_info_tuple[0]
            if predicate == property_name:
                hit_property_name = property_name
                break
            similarity = predicate_match_dict(predicate, property_name)
            if similarity:
                hit_property_name = property_name
                break
        # rule
        if not hit_property_name:
            if predicate == '长度':
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    if '长' in property_name:
                        hit_property_name = property_name
                        # print('rule hit')
                        break
            elif predicate == '高度':
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    if '身高' in property_name:
                        hit_property_name = property_name
                        break
                    if '高' in property_name:
                        hit_property_name = property_name
                # print('rule hit')
            elif predicate in ['地点', '国家', '城市']:
                location_def_list = ['地点', '地区', '位置', '国籍', '所属洲']   # delete 城市 国家 add 所属洲
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    for location_def in location_def_list:
                        if location_def in property_name:
                            hit_property_name = property_name
                            # print('rule hit')
                            break
                    if hit_property_name:
                        break
            elif predicate in ['提出', '发现', '发明']:
                predicate_def_list = ['提出', '发现', '发明']
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    for predicate_def in predicate_def_list:
                        if predicate_def in property_name:
                            hit_property_name = property_name
                            # print('rule hit')
                            break
                    if hit_property_name:
                        break
            elif predicate in ['发生时间', '时间', '发生时代']:
                predicate_def_list = ['发生时间', '时间', '发生时代']
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    for predicate_def in predicate_def_list:
                        if predicate_def == property_name:
                            hit_property_name = property_name
                            # print('rule hit')
                            break
                    if hit_property_name:
                        break
            elif predicate in ['作品', '主要作品', '代表作品']:
                predicate_def_list = ['作品', '主要作品', '代表作品']
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    for predicate_def in predicate_def_list:
                        if predicate_def == property_name:
                            hit_property_name = property_name
                            # print('rule hit')
                            break
                    if hit_property_name:
                        break
            elif predicate in ['生日', '出生日期', '出生时间']:
                predicate_def_list = ['生日', '出生日期', '出生时间']
                for entity_info_tuple in entity_info_list:
                    property_name = entity_info_tuple[0]
                    for predicate_def in predicate_def_list:
                        if predicate_def == property_name:
                            hit_property_name = property_name
                            # print('rule hit')
                            break
                    if hit_property_name:
                        break
        # semantic
        if not hit_property_name:
            for entity_info_tuple in entity_info_list:
                property_name = entity_info_tuple[0]
                similarity = get_similarity(predicate, property_name)
                # print('{} {} {}'.format(predicate, property_name, similarity))
                if similarity > 0.6:
                    hit_property_name = property_name
                    # print('kg semantic hit')
                    break

        # append value
        if hit_property_name:
            for entity_info_tuple in entity_info_list:
                property_name = entity_info_tuple[0]
                property_value = entity_info_tuple[1]
                if property_name == hit_property_name:
                    candidate_list.append(property_value)
            rst_list.append({'candidate_list': candidate_list, 'disambiguation': ''})
            break
    #print(rst_list)
    return rst_list


def search_object_service_fuzzy(subject, predicate, object):
    '''
    search object in spo, given s and p, fuzzy match with predicate
    :param subject:
    :param predicate:
    :return:
    '''

    if object == "x?":
        rst_list = kg_search(subject, predicate, object)
        return rst_list
    else:
        return check_object(subject, predicate, object)


def predicate_match_dict(predicate_query, predicate_entity):
    query_synonym = schema_dao.search_node_synonym_dict(predicate_query)
    entity_synonym = schema_dao.search_node_synonym_dict(predicate_entity)
    for query_cell in query_synonym:
        if query_cell in entity_synonym:
            return True
    for entity_cell in entity_synonym:
        parent_query = schema_dao.search_node_parent_dict(entity_cell)
        for query_cell in query_synonym:
            if query_cell in parent_query:
                return True
    return False


def entity_search(keyword):
    # service for web api
    entity_list = []
    synonym_id_list = kg_dao.search_node(['Synonym'], {'name': keyword})
    if synonym_id_list:
        synonym_id = synonym_id_list[0]
        rel_list = kg_dao.search_relationship(synonym_id, 'out')
        count = 0
        # add default firstly
        for rel in rel_list:
            rel_properties = rel[1]
            if 'default' in rel_properties:
                node_id = rel[0]
                node_name = kg_dao.get_node_property_value(node_id, 'name')
                disambiguation_list = kg_dao.get_node_property_value(node_id, 'disambiguation')
                node_disambiguation = ', '.join(disambiguation_list)
                entity_list.append([node_name, node_disambiguation])
        # add others
        for rel in rel_list:
            rel_properties = rel[1]
            if 'default' in rel_properties:
                continue
            count += 1
            if count > 9:
                break
            node_id = rel[0]
            node_name = kg_dao.get_node_property_value(node_id, 'name')
            disambiguation_list = kg_dao.get_node_property_value(node_id, 'disambiguation')
            node_disambiguation = ', '.join(disambiguation_list)
            entity_list.append([node_name, node_disambiguation])
    return {'entity_list': entity_list}


def entity_info(node_name, node_disambiguation):
    # service for web api
    triple_list = []
    abstract = ''
    node_id_list = kg_dao.search_node(['Entity'], {'name': node_name})
    if len(node_id_list) == 1:
        node_id = node_id_list[0]
        # 返回所属性和关系
        triple_list, abstract = kg_dao.get_node_all_triples(node_id)
    else:
        for node_id in node_id_list:
            disambiguation_list = kg_dao.get_node_property_value(node_id, 'disambiguation')
            disambiguation = ', '.join(disambiguation_list)
            if disambiguation == node_disambiguation:
                # 返回所属性和关系
                triple_list, abstract = kg_dao.get_node_all_triples(node_id)
                break
    abstract = abstract_full_clean(abstract)
    return {'abstract': abstract, 'triples': triple_list}


def get_abstract(entity_info_list, limit=10000):
    node_name = ''
    url = ''
    abstract = ''
    tag_subject = []
    for entity_info_tuple in entity_info_list:
        property_name = entity_info_tuple[0]
        property_value = entity_info_tuple[1]
        if property_name == 'url':
            url = property_value
        elif property_name == 'Tag':
            tag_subject.append(property_value)
        elif property_name == 'name':
            node_name = property_value
        elif property_name == 'abstract':
            abstract = property_value

    # Todo: 随机取两个
    if len(tag_subject) >= 2:
        tag_subject = random.sample(tag_subject, 2)
    ans = ''
    for tag_cell in tag_subject:
        ans = tag_cell + '，' + ans
    regex_1 = u'（.*），'
    regex_2 = u'\\[(\\d|\\-)+\\]'

    pattern_list = ['"' + node_name + '"', '“' + node_name + '”', '《' + node_name + '》', node_name]
    for pattern in pattern_list:
        if abstract[:len(pattern)] == pattern:
            abstract = abstract[len(pattern):]
            break
    ans += abstract
    ans = re.sub(regex_2, "", ans)
    ans = ans.replace(u",", "，")
    ans = ans.replace(u"，，", "，")
    ans_split = ans.strip().split('。')

    ans = ""
    for ans_cell in ans_split:
        if len(ans) >= limit:
            break
        else:
            ans += ans_cell
            ans += "。"
    ans = ans.replace(u"。。", "。")
    if ans[-1] == '，':
        ans = ans[:-1]
    return ans


def abstract_full_clean(abstract_raw, limit=10000):
    if not abstract_raw:
        return ''
    ans = ''
    regex_1 = u'（.*），'
    regex_2 = u'\\[(\\d|\\-)+\\].'
    ans += abstract_raw
    ans = re.sub(regex_2, "", ans)
    ans = ans.replace(u",", "，")
    ans = ans.replace(u"，，", "，")
    ans = ans.strip()
    ans_split = ans.strip().split('。')

    ans = ""
    for ans_cell in ans_split:
        if len(ans) >= limit:
            break
        else:
            ans += ans_cell
            ans += "。"
    ans = ans.replace(u"。。", "。")
    if ans[-1] == '，':
        ans = ans[:-1]
    return ans


def check_object(subject, predicate, object):
    """
    :param object:
    :return:
    """
    if "subject_compare:" in object:
        rst_list = kg_search(subject, predicate, object)
        return check_compare_question(object, predicate, rst_list)
    if "subject_jump:" in object:
        rst_list = check_jump_question(subject, predicate, object)
        if rst_list != []:
            return rst_list
        else:
            predicate = predicate.replace("subject_jump", "subject_updown")
            return check_updown_question(subject, predicate, object)
    if "subject_updown:" in object:
        return check_updown_question(subject, predicate, object)
    rst_list = kg_search(subject, predicate, object)
    if "/" in object and "//" not in object and u"元" not in object and u"平" not in object:
        object = check_object_time(object)
    object = object
    rst_list_new = []
    for res_list_cell in rst_list:
        answer = res_list_cell['candidate_list']
        for answer_cell in answer:
            if answer_cell.find(object) != -1:
                res_list_cell['object_label'] = 'yes'
                break
        rst_list_new.append(res_list_cell)
    return rst_list_new


def check_updown_question(subject, predicate, object):
    object = object.replace("subject_updown:", "")
    rst_list = []
    all_candi = []
    all_candi += kg_dao.search_node_by_entity_and_relation(subject, predicate, object, "Tag")
    rst_list.append({'candidate_list': all_candi, 'disambiguation': None})
    return rst_list


def check_jump_question(subject, predicate, object):
    subject_jump = object.replace("subject_jump:", "")
    rst_list_subject_jump = kg_search(subject, subject_jump, "x?")
    if len(rst_list_subject_jump) != 0:
        subject_jump_value = rst_list_subject_jump[0]['candidate_list'][0]
        rst_list = kg_search(subject_jump_value, predicate, "x?")
    else:
        rst_list = []
    return rst_list


def check_compare_question(object, predicate, rst_list):
    # print('subject_compare')
    subject_compare = object.replace("subject_compare:", "")
    rst_list_compare = kg_search(subject_compare, predicate, "x?")
    if len(rst_list_compare) != 0 and len(rst_list) != 0:
        value_subject = rst_list[0]['candidate_list'][0]
        value_subject_compare = rst_list_compare[0]['candidate_list'][0]
    # print(value_subject)
    # print(value_subject_compare)
        if u"平方" in value_subject and u"平方" in value_subject_compare:
            bool_compare = check_compare_area(value_subject, value_subject_compare)
        elif (predicate == u"学历"):
            bool_compare = check_compare_education(value_subject, value_subject_compare)
        elif (u"元" in value_subject and u"元" in value_subject_compare):
            bool_compare = check_compare_money(value_subject, value_subject_compare)
        else:
            bool_compare = check_compare_general(value_subject, value_subject_compare)
        rst_list[0]["bool_compare"] = bool_compare
        return [rst_list[0]]
    else:
        return []


def check_compare_money(value_subject, value_subject_compare):
    value = [value_subject, value_subject_compare]
    number_list = []
    for value_cell in value:
        number = re.search("(\\d+)", value_cell).group(1)
        number = float(number)
        if u"亿" in value_cell:
            number = number * 100000000
        elif (u"万" in value_cell):
            number = number * 10000
        else:
            number = number
        if u"美元" in value_cell:
            number = number * 6.9
        elif (u"日元" in value_cell):
            number = number / 16.3
        number_list.append(number)
    value_subject = number_list[0]
    value_subject_compare = number_list[1]
    if value_subject > value_subject_compare:
        return True
    elif (value_subject_compare == value_subject):
        return "Same"
    else:
        return False


def check_compare_education(value_subject, value_subject_compare):
    education_dict = {u"博士后": 0, u"博士": 1, u"硕士": 2, u"研究生": 3, u"本科": 4, u"大学生": 4, u"学士": 4, u"专科": 5, u"高中": 6,
                      u"中专": 7, u"初中": 8, u"小学": 9}
    value_subject_list = []
    value_subject_compare_list = []
    for education_key, education_value in education_dict.items():
        if education_key in value_subject:
            value_subject_list.append(education_value)
        if education_key in value_subject_compare:
            value_subject_compare_list.append(education_value)
    value_subject_list.append(9999)
    value_subject_compare_list.append(9999)
    value_subject_list = sorted(value_subject_list)
    value_subject_compare_list = sorted(value_subject_compare_list)
    value_subject = value_subject_list[0]
    value_subject_compare = value_subject_compare_list[0]
    if value_subject < value_subject_compare:
        return True
    elif (value_subject == value_subject_compare):
        return "Same"
    else:
        return False


def check_compare_general(value_subject, value_subject_compare):
    value_subject = re.search(u"(\\d+)", value_subject)
    value_subject_compare = re.search(u"(\\d+)", value_subject_compare)
    if value_subject and value_subject_compare:
        value_subject = value_subject.group()
        value_subject_compare = value_subject_compare.group()
        if float(value_subject) > float(value_subject_compare):
            return True
        elif (float(value_subject) == float(value_subject_compare)):
            return "Same"
    else:
        return False


def check_compare_area(value_subject, value_subject_compare):
    regex_1 = u"(.+)(平方公里|平方千米)"
    regex_2 = u"(.+)(平方米)"
    if re.search(regex_1, value_subject):
        value_subject = re.search(regex_1, value_subject).group(1)
        if u"陆地面积" in value_subject:
            value_subject = value_subject.strip(u"陆地面积")
        if value_subject[-1] == u"万":
            value_subject = value_subject[:-1]
            value_subject = float(value_subject) * 10000
        value_subject = float(value_subject) * 1000
    elif (re.search(regex_2, value_subject)):
        value_subject = re.search(regex_2, value_subject).group(1)
        value_subject = cn2dig(value_subject)
        value_subject = float(value_subject)

    if re.search(regex_1, value_subject_compare):
        value_subject_compare = re.search(regex_1, value_subject_compare).group(1)
        if value_subject_compare[-1] == u"万":
            value_subject_compare = value_subject_compare[:-1]
            value_subject_compare = float(value_subject_compare) * 10000
        # value_subject_compare = cn2dig(value_subject_compare)
        value_subject_compare = float(value_subject_compare) * 1000
    elif (re.search(regex_2, value_subject_compare)):
        value_subject_compare = re.search(regex_2, value_subject_compare).group(1)
        value_subject_compare = cn2dig(value_subject_compare)
        value_subject_compare = float(value_subject_compare)

    if value_subject > value_subject_compare:
        return True
    elif (value_subject == value_subject_compare):
        return "Same"
    else:
        return False


def check_object_time(object):
    object = str(object)
    object = object.split('/')
    if len(object) == 3:
        if object[1].isdigit() and object[2].isdigit():
            object = object[0] + u'年' + str(int(object[1])) + u'月' + str(int(object[2])) + u'日'
    return object


if __name__ == "__main__":
    rst = entity_info('流浪地球', '中国2019年郭帆执导电影')
    print(rst)
