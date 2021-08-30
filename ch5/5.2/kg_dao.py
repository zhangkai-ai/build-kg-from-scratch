#!/usr/bin/env python

import re
import os
from neo4j.v1 import GraphDatabase, basic_auth


class KGDao:
    def __init__(self):
        # neo4j_dict = current_app.config.get('neo4j')
        neo4j_dict = {
            'bolt': os.environ.get('NEO4J_URL', 'bolt://localhost:7789'),
            'user': 'neo4j',
            'pwd': 'neo4j'
        }
        self.kg_driver = GraphDatabase.driver(neo4j_dict['bolt'],
                                              auth=basic_auth(neo4j_dict['user'], neo4j_dict['pwd']))
        self.kg_session = self.kg_driver.session()

    def close(self):
        self.kg_driver.close()

    def reset(self):
        cql = 'match ()-[r]-() delete r'
        self.kg_session.run(cql)
        cql = 'match (n) delete n'
        self.kg_session.run(cql)

    def get_node_property_value(self, node_id, property_name):
        '''
        get property_value of a neo4j node with node_id and property_name
        :param node_id: neo4j node ID
        :param property_name: neo4j node property name
        :return: property_value
        '''
        property_value = ''
        # excute cql
        cql = 'MATCH (n) WHERE ID(n)={} return n.{}'.format(node_id, property_name)
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            property_value = record['n.{}'.format(property_name)]
        return property_value

    def get_node_properties(self, node_id):
        '''
        get property_value of a neo4j node with node_id and property_name
        :param node_id: neo4j node ID
        :return: property_value
        '''
        property_dict = {}
        # excute cql
        cql = 'MATCH (n) WHERE ID(n)={} return properties(n)'.format(node_id)
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            property_dict = record['properties(n)']
        return property_dict

    def create_node(self, label_list, property_map, is_merge=True):
        '''
        create a neo4j node with labels and properties
        :param label_list: neo4j node labels.
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
        cql_result = self.kg_session.run(cql)
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
        self.kg_session.run(cql)
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
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            node_id_list.append(record['ID(n)'])
        return node_id_list

    def traverse_node_by_type(self, node_type):
        '''
        traverse nodes by type
        :param node_type:
        :return: list of the neo4j node name
        '''
        node_name_synonym_dict = {}
        # excute cql
        cql = 'MATCH (n:{}) return n.name, n.synonym, ID(n)'.format(node_type)
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            node_name_synonym_dict[record['n.name']] = (record['n.synonym'], record['ID(n)'])
        return node_name_synonym_dict

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
        # self.kg_session.run(cql)
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            pass
            # print(record)
        # pass

    def create_relationship_with_type(self, node_id_1, node_id_2, rel_type, property_map):
        '''
        create a neo4j relationship with properties and default type
        :param node_id_1:
        :param node_id_2:
        :param rel_type:
        :param property_map:
        :return:
        '''
        # generate property string to insert cql
        property_string = self.generate_property_string(property_map)
        # excute cql
        cql = 'MATCH(node_1) WHERE ID(node_1)={} ' \
              'MATCH(node_2) WHERE ID(node_2)={} ' \
              'MERGE (node_1)-[:{} {}]->(node_2)'\
            .format(node_id_1, node_id_2, rel_type, property_string)
        # self.kg_session.run(cql)
        cql_result = self.kg_session.run(cql)
        for record in cql_result:
            pass
            # print(record)
        # pass

    def delete_relationship(self, node_id):
        '''
        delete all relationships of a node
        :param node_id:
        :return:
        '''
        # excute cql
        cql = 'MATCH (n)-[r]-() WHERE ID(n)={} DELETE r'.format(node_id)
        self.kg_session.run(cql)
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
        self.kg_session.run(cql)
        pass

    def generate_property_string(self, property_map):
        '''
        generate property string to insert cql
        :param property_map:
        :return: property string for cql
        '''
        if not property_map:
            return ''
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
                elif len(property_value) == 0:
                    property_string += '{}:[],'.format(key)
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



kg_dao = KGDao()
