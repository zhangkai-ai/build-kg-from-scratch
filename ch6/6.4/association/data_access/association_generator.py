#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
相关话题生成
"""
from loguru import logger
from neo4j.v1 import GraphDatabase, basic_auth
from gensim.models import KeyedVectors
from util.entity_linker import entity_linking


model = KeyedVectors.load_word2vec_format("vec.bin", binary=True)
username = "neo4j"
pwd = "neo4j"
kg_driver = GraphDatabase.driver("bolt://192.168.1.110:7687", auth=basic_auth(username, pwd))
kg_session = kg_driver.session()


def get_association_by_kg(topic, sent):
    """
    基于kg生成相关话题功能函数
    :param topic: 待关联话题
    :param sent: 输入语句，即上下文
    :return: 候选关联话题列表
    """
    candidate_list = []
    node_id = entity_linking(topic, sent)
    cql = "MATCH p=(n)-[r]-(e) WHERE ID(n)={} RETURN e.name".format(node_id)
    cql_result = kg_session.run(cql)
    for record in cql_result:
        candidate_list.append(record["e.name"])
    return candidate_list


def get_association_by_embedding(topic, top_k=5):
    """
    基于词向量生成相关话题功能函数
    :param topic: 待关联话题
    :param top_k: 待关联的话题数量
    :return: 候选关联话题列表
    """
    candidate_list = []
    try:
        candidate_list = model.most_similar(positive=[topic], topn=top_k)
    except Exception as e:
        logger.exception(e)
    return candidate_list
