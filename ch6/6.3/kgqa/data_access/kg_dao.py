#!/usr/bin/env python
# -*- coding:utf8 -*-

import json
import re
import sys
import  configparser
from neo4j.v1 import GraphDatabase, basic_auth
# reload(sys)
# sys.setdefaultencoding('utf-8')


class KGDao:
    def __init__(self, kg_name):
        __cf = configparser.ConfigParser()
        __cf.read("./config.ini")
        __db_username = 'user1'
        __db_pwd = '123456' # 密码
        self.baike_driver = GraphDatabase.driver(__cf.get("kg", "bolt_" + kg_name),
                                                       auth=basic_auth(__db_username, __db_pwd))
        self.baike_session = self.baike_driver.session()
        self.children2parent_dict = {}
        self.synonym_dict = {}
        self.synonym_dict_reverse = {}

    # def __del__(self):
    #     self.baike_session.close()
    #     self.baike_driver.close()

    def search_spo(self, subject_id, predicate):
        '''
        通过subject_id和predicate查询object的值
        :param subject_id:
        :param predicate:
        :return:
        '''
        value = self.get_node_property_value(subject_id, predicate)
        if value:
            return value
        value_id = self.get_node_relation(subject_id, predicate)
        if value_id:
            value = self.get_node_name(value_id)
            # 若能匹配成功，返回True
            if value in object or object in value:
                return value
        return None

    def get_node_relation(self, node_id, predicate):
        pass

    def get_node_name(self, node_id):
        pass

    def get_node_property_value(self, node_id, property_name):
        '''
        get property_value of a neo4j node with node_id and property_name
        :param node_id: neo4j node ID
        :param property_name:
        :return: property_value
        '''
        property_value = ''
        # excute cql
        cql = 'MATCH (n) WHERE ID(n)={} return n.{}'.format(node_id, property_name)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            property_value = record['n.{}'.format(property_name)]
        return property_value

    def create_node(self, label_list, property_map, is_merge=True):
        '''
        create a neo4j node with labels and properties
        :param label_list:
        :param property_map:
        :param is_merge: True->MERGE mode; False->CREATE mode
        :return: the newly created node ID
        '''
        # generate label string to insert cql
        label_string = ''
        for label in label_list:
            label_string += (':' + label)
        # generate property string to insert cql
        property_string = self.generate_property_string(property_map)
        # excute cql
        node_id = 0
        if is_merge:
            cql = 'MERGE (n{} {}) return ID(n)'.format(label_string, property_string)
        else:
            cql = 'CREATE (n{} {}) return ID(n)'.format(label_string, property_string)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            node_id = record['ID(n)']
        return node_id

    def delete_node(self, node_id):
        '''
        delete a node with node_id
        :param node_id:
        :return:
        '''
        # excute cql
        cql = 'MATCH (n) WHERE ID(n)={} DELETE n'.format(node_id)
        self.baike_session.run(cql)
        pass

    def search_node(self, label_list, property_map):
        '''
        search for neo4j nodes matching with label and property
        :param label_list:
        :param property_map:
        :return: list of the neo4j node ID
        '''
        node_id_list = []
        # generate label string to insert cql
        label_string = ''
        for label in label_list:
            label_string += (':' + label)
        # generate property string to insert cql
        property_string = self.generate_property_string(property_map)
        # excute cql
        cql = 'MATCH (n{} {}) return ID(n)'.format(label_string, property_string)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            node_id_list.append(record['ID(n)'])
        return node_id_list

    def create_relationship(self, node_id_1, node_id_2, property_map):
        '''
        create a neo4j relationship with properties and default type
        :param node_id_1:
        :param node_id_2:
        :param property_map:
        :return:
        '''
        # generate property string to insert cql
        property_string = self.generate_property_string(property_map)
        # excute cql
        cql = 'MATCH(node_1) WHERE ID(node_1)={} ' \
              'MATCH(node_2) WHERE ID(node_2)={} ' \
              'MERGE (node_1)-[:r {}]->(node_2)'\
            .format(node_id_1, node_id_2, property_string)
        self.baike_session.run(cql)
        pass

    def delete_relationship(self, node_id):
        '''
        delete all relationships of a node
        :param node_id:
        :return:
        '''
        # excute cql
        cql = 'MATCH (n)-[r]-() WHERE ID(n)={} DELETE r'.format(node_id)
        self.baike_session.run(cql)
        pass

    def delete_one_relationship(self, node_id_1, node_id_2, direct_mode=None):
        '''
        delete all relationships with node_id of two nodes
        :param node_id_1:
        :param node_id_2:
        :param direct_mode: 'in'; 'out'; None means no constraint
        :return:
        '''
        # excute cql
        if direct_mode == 'out':
            cql = 'MATCH(node_1)-[r]->(node_2) WHERE ID(node_1)={} and ID(node_2)={} delete r'\
                .format(node_id_1, node_id_2)
        elif direct_mode == 'in':
            cql = 'MATCH(node_1)<-[r]-(node_2) WHERE ID(node_1)={} and ID(node_2)={} delete r'\
                .format(node_id_1, node_id_2)
        else:
            cql = 'MATCH(node_1)-[r]-(node_2) WHERE ID(node_1)={} and ID(node_2)={} delete r'\
                .format(node_id_1, node_id_2)
        self.baike_session.run(cql)
        pass

    def dump_relationship(self):
        '''
        search all in neo4j relationship of one node with node_id
        :param node_id:
        :param direct_mode: 'in'; 'out'; None means no constraint
        :return:
        '''
        relationship_list = []
        cql = "MATCH p=(n:synonym)-[r]->(e:synonym) RETURN n.name, type(r), e.name"
        cql_result = self.baike_session.run(cql)

        name_entity = []
        for record in cql_result:
            entity_1 = record["n.name"]
            relation = record["type(r)"]
            entity_2 = record["e.name"]
            #name_entity = name_entity + [entity_1]
            #name_entity = name_entity + [entity_2]
            if relation == "children":
                self.children2parent_dict[entity_2] = entity_1
            else:
                self.synonym_dict[entity_1] = list(self.synonym_dict.get(entity_1,[])) + [entity_2]
                self.synonym_dict_reverse[entity_2] = list(self.synonym_dict.get(entity_2,[])) + [entity_1]
        name_entity = set(name_entity)
        #print name_entity
        return

    def search_node_synonym_dict(self, sent):
        '''
        返回查询节点的同义表述
        :param sent:
        :return:
        '''
        sent_synonym = self.synonym_dict.get(sent,None)
        sent_synonym_reverse = self.synonym_dict_reverse.get(sent,None)

        synonym_entity = []
        if sent_synonym is not None:
            synonym_entity += sent_synonym
        if sent_synonym_reverse is not None:
            synonym_entity += sent_synonym_reverse
        synonym_entity += [sent]

        return synonym_entity

    def search_node_parent_dict(self, sent):
        parent_all = []
        parent = self.children2parent_dict.get(sent,[])
        while True:
            if parent:
                parent_all.append(parent)
                parent = self.children2parent_dict.get(parent,[])
            else:
                break
        return parent_all

    def search_relationship(self, node_id, direct_mode=None):
        '''
        search all in neo4j relationship of one node with node_id
        :param node_id:
        :param direct_mode: 'in'; 'out'; None means no constraint
        :return:
        '''
        relationship_list = []
        if direct_mode == 'out':
            cql = "MATCH p=(n)-[r]->(e) WHERE ID(n)={} RETURN r, ID(e)".format(node_id)
        elif direct_mode == 'in':
            cql = "MATCH p=(n)<-[r]-(e) WHERE ID(n)={} RETURN r, ID(e)".format(node_id)
        else:
            cql = "MATCH p=(n)-[r]-(e) WHERE ID(n)={} RETURN r, ID(e)".format(node_id)

        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            out_node_id = record["ID(e)"]
            properties = record["r"].properties
            if out_node_id != node_id:
                relationship_list.append((out_node_id, properties))
        return relationship_list

    def search_node_by_relationship(self, node_id, rel_name, direct_mode=None):
        '''
        search all relation nodes of one node with node_id and rel_name
        :param node_id:
        :param rel_name:
        :param direct_mode: 'in'; 'out'; None means no constraint
        :return: node_id_name_list
        '''
        node_id_name_list = []
        if direct_mode == 'out':
            cql = "MATCH p=(n)-[r]->(e) WHERE ID(n)={} and r.name=\'{}\' RETURN ID(e), e.name".format(node_id, rel_name)
        elif direct_mode == 'in':
            cql = "MATCH p=(n)<-[r]-(e) WHERE ID(n)={} and r.name=\'{}\' RETURN ID(e), e.name".format(node_id, rel_name)
        else:
            cql = "MATCH p=(n)-[r]-(e) WHERE ID(n)={} and r.name=\'{}\' RETURN ID(e), e.name".format(node_id, rel_name)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            node_id_name_list.append((record["ID(e)"], record["e.name"]))
        return node_id_name_list

    def search_node_by_relationship_type(self, node_id, rel_type, direct_mode=None):
        '''
        search all relation nodes of one node with node_id and rel_type
        :param node_id:
        :param rel_type:
        :param direct_mode: 'in'; 'out'; None means no constraint
        :return: node_id_name_list
        '''
        node_id_name_list = []
        if direct_mode == 'out':
            cql = "MATCH p=(n)-[r]->(e) WHERE ID(n)={} and type(r)=\'{}\' RETURN ID(e), e.name".format(node_id, rel_type)
        elif direct_mode == 'in':
            cql = "MATCH p=(n)<-[r]-(e) WHERE ID(n)={} and type(r)=\'{}\' RETURN ID(e), e.name".format(node_id, rel_type)
        else:
            cql = "MATCH p=(n)-[r]-(e) WHERE ID(n)={} and type(r)=\'{}\' RETURN ID(e), e.name".format(node_id, rel_type)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            node_id_name_list.append((record["ID(e)"], record["e.name"]))
        return node_id_name_list

    def get_tag_by_subject(self, subject_id):
        node_name_list=[]
        cql = "MATCH p=(n)-[r]->(e:Tag) where ID(n) = {} RETURN e.name".format(subject_id)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            node_name_list.append(record["e.name"])
        return node_name_list

    def search_node_by_entity_and_relation(self, subject, predicate, object, relation):
        """
        :return:
        """
        node_name_list = set()
        cql_1 = 'MATCH p=(n:Synonym{name:"' + subject + '"})-[:r{default:1}]-()-[:r{name:"' + predicate + '"}]-(e)-[:r{name:"Tag"}]-(:Tag{name:"' + object + '"}) RETURN e.name'
        cql_2 = 'MATCH p=(n:Synonym{name:"' + subject + '"})-[:r{default:1}]-()-[:r{name:"' + predicate + '"}]-(:Synonym)-[:r]->(e)-[:r{name:"Tag"}]-(:Tag{name:"' + object + '"}) RETURN e.name'
        # cql = "MATCH p=(n:Entity)-[r]->(e:Entity)-[]->(b:Tag) where n.name = '{}' and r.name = '{}' and b.name = '{}' RETURN e.name".format(subject, predicate, object)
        cql_result_1 = self.baike_session.run(cql_1)
        cql_result_2 = self.baike_session.run(cql_2)
        for record_1 in cql_result_1:
            node_name_list.add(record_1["e.name"])
        for record_2 in cql_result_2:
            node_name_list.add(record_2["e.name"])
        return list(node_name_list)

    def generate_property_string(self, property_map):
        '''
        generate property string to insert cql
        :param property_map:
        :return: property string for cql
        '''
        property_string = '{'
        for key in property_map:
            # property_map may contains string value or list value
            property_value = property_map[key]
            match = re.match(r'\d', key[0])
            if match:
                key = 'todo' + key
            if type(property_value) == list:
                if len(property_value) == 1:
                    property_string += '{}:\'{}\','.format(key, self.special_str_handler(str(property_value[0])))
                else:
                    list_string = '['
                    for value in property_value:
                        list_string += '\'{}\','.format(self.special_str_handler(str(value)))
                    list_string = list_string[:-1] + ']'
                    property_string += '{}:{},'.format(key, list_string)
            else:
                property_string += '{}:\'{}\','.format(key, self.special_str_handler(str(property_value)))
        property_string = property_string[:-1] + '}'
        return property_string

    def special_str_handler(self, str_old):
        '''
        filter special str for cypher
        :param str_old:
        :return: filtered new str
        '''
        str_new = str_old
        str_new = str_new.replace('\\', '\\\\')
        str_new = str_new.replace('\'', '\\\'')
        return str_new

    def get_all_definitions(self):
        '''
        get all definitions of baike kg including node_name and property_name
        :return: node_name_list and property_name_list
        '''
        node_name_set = set()
        property_name_set = set()
        # node
        cql = "MATCH (n) RETURN properties(n)"
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            property_map = record["properties(n)"]
            node_name_set.add(property_map['name'])
            for property_key in property_map:
                property_name_set.add(property_key)
        # relationship
        cql = "MATCH ()-[r]-() RETURN r.name"
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            property_name_set.add(record['r.name'])

        return node_name_set, property_name_set

    def get_node_all_infos(self, node_id):
        '''
        get all info of a node, including property and relation
        :param node_id: node_id
        :return: node_name_list and property_name_list
        '''
        property_name_set = set()
        relation_name_set = set()
        # node
        cql = 'MATCH (n) WHERE ID(n)={} return properties(n)'.format(node_id)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            property_map = record["properties(n)"]
            for property_key in property_map:
                property_name_set.add(property_key)
        # relationship
        cql = "MATCH (n)-[r]->() WHERE ID(n)={}  RETURN r.name".format(node_id)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            relation_name_set.add(record['r.name'])
        return property_name_set, relation_name_set

    def get_node_all_triples(self, node_id):
        '''
        get all triples of a node, including property and relation
        :param node_id: node_id
        :return: property and relation list
        '''
        triple_list = []
        abstract = ''
        # property
        cql = 'MATCH (n) WHERE ID(n)={} return properties(n)'.format(node_id)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            property_map = record["properties(n)"]
            for property_key in property_map:
                if property_key == 'abstract':
                    abstract = property_map[property_key]
                    continue
                if property_key not in ['name', 'url_str', 'url_num', 'disambiguation']:
                    if type(property_map[property_key]) == list:
                        for property_value in property_map[property_key]:
                            triple_list.append([property_key, property_value])
                    else:
                        triple_list.append([property_key, property_map[property_key]])
        # relationship
        cql = "MATCH (n)-[r]->(e) WHERE ID(n)={}  RETURN r.name, e.name".format(node_id)
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            if record['r.name'] != 'Tag':
                triple_list.append([record['r.name'], record['e.name']])
        return triple_list, abstract

    def search_node_info_by_name(self, entity_name):
        '''
        通过实体名称返回实体结点的id以及属性和关系的三元组信息
        :param entity_name:
        :return:
        '''
        id_info_dict = {}
        default_id_set = set()
        entity_info_list = []
        # property查询
        # 返回entity_name的所有同义词表述所在的实体信息
        cql = 'MATCH (n:Synonym{name:"' + entity_name + '"})-[r:r]->(e:Entity) return id(e), r.default, properties(e)'
        cql_rst = self.baike_session.run(cql)
        for record in cql_rst:
            entity_id = record['id(e)']
            property_map = record['properties(e)']
            if record['r.default']:
                default_id_set.add(entity_id)
            triple_list = []
            url_str = ''
            url_num = ''
            for property_key in property_map:
                if type(property_map[property_key]) == list:
                    for property_value in property_map[property_key]:
                        triple_list.append([property_key, property_value])
                else:
                    triple_list.append([property_key, property_map[property_key]])
                    if property_key == 'url_str':
                        url_str = property_map[property_key]
                    elif property_key == 'url_num':
                        url_num = property_map[property_key]
            if url_num:
                url = url_str + '/' + url_num
            else:
                url = url_str
            triple_list.append(['id', entity_id])
            triple_list.append(['url', url])
            id_info_dict[entity_id] = triple_list

        # relationship
        cql = 'MATCH (n:Synonym{name:"' + entity_name + '"})-[r:r]->(e:Entity)-[k:r]->(ke) return id(e), k.name, ke.name'
        cql_result = self.baike_session.run(cql)
        for record in cql_result:
            entity_id = record['id(e)']
            triple_list = id_info_dict[entity_id]
            triple_list.append([record['k.name'], record['ke.name']])
        # generate
        for default_id in default_id_set:
            entity_info_list.append(id_info_dict[default_id])
        for entity_id in id_info_dict:
            if entity_id not in default_id_set:
                entity_info_list.append(id_info_dict[entity_id])

        return entity_info_list


kg_dao = KGDao('baike')
acgn_kg_dao = KGDao('acgn')
schema_dao = KGDao('schema')
schema_dao.dump_relationship()

if __name__ == "__main__":
    sent = '员工'
    # schema_dao.search_node_children_dict(sent)
