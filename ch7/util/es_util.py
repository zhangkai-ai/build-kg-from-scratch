#!/usr/bin/env python
# -*- coding:utf8 -*-
from elasticsearch import Elasticsearch


class ESUtil:
    def __init__(self, host, port):
        # 创建es数据库连接对象
        # self.es = Elasticsearch(host=host, port=port, timeout=5, retry_on_timeout=False)  # deprecated in 8.x es-client
        self.es = Elasticsearch(f"http://{host}:{port}", timeout=5, retry_on_timeout=False)

    def query(self, text, index, confidence=0):
        """
        基于text，查询匹配的document
        :param text: 待匹配文本
        :param index: index名称
        :param confidence: 要求的查询置信度最小值
        :return:
        """
        query_body = {
            "query": {
                "match": {
                    "query": text,
                    "minimum_should_match": "60%"
                }
            }
        }
        res = self.es.search(index=index, size=10, request_timeout=3, body=query_body)
        if res['hits']['total'] > 0:
            valid = filter(lambda x: x['_score'] >= confidence,
                           [hit for hit in res['hits']['hits']])
            if not valid:
                return None
            else:
                matched_list = []
                for valid_dict in valid:
                    matched_question = valid_dict['_source']['question']
                    matched_answer = valid_dict['_source']['answer']
                    matched_score = valid_dict['_score']
                    matched_list.append([matched_question, matched_answer, matched_score])
                return matched_list


es_object = ESUtil("192.168.1.110", 9400)
