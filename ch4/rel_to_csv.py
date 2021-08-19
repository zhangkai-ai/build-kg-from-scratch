#!/usr/bin/env python
# -*- coding:utf8 -*-

import csv

data_list = [
    ("Subject", "Predicate", "Object"),
    (1, "董事长", 0),
    (1, "CEO", 0),
    (1, "isA", 4),
]

with open('rel.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(data_list)

