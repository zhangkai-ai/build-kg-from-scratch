#!/usr/bin/env python
# -*- coding:utf8 -*-

import hnswlib


class HNSWUtil(object):
    def __init__(self, dim=128, num_elements=10000):
        # Declaring index
        self.p = hnswlib.Index(space='l2', dim=dim)  # possible options are l2, cosine or ip
        # Initing index - the maximum number of elements should be known beforehand
        self.p.init_index(max_elements=num_elements, ef_construction=200, M=16)
        # Controlling the recall by setting ef:
        self.p.set_ef(50)  # ef should always be > k

    def insert(self, data, data_labels):
        # Element insertion (can be called several times):
        self.p.add_items(data, data_labels)

    def query(self, data):
        # Query dataset, k - number of closest elements (returns 2 numpy arrays)
        labels, distances = self.p.knn_query(data, k=1)
        return labels, distances


hnsw_object = HNSWUtil()
