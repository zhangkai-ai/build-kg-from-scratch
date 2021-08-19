#!/usr/bin/env python
# -*- coding:utf8 -*-
import json

node_dict = {
    "name": "北京小米科技有限责任公司",
    "label": ["Entity"],
    "url_name": "北京小米科技有限责任公司",
    "url_id": "3250213",
    "disambiguation": "小米公司",
    "成立时间": "2010-3",
    "公司口号": ["小米为发烧而生", "探索黑科技"]
}
# node_json_str = json.dumps(node_dict, ensure_ascii=False)
# with open("test_node_file.txt", "w") as f_out:
#     f_out.write(node_json_str + "\n")

node_json_str = json.dumps(node_dict, ensure_ascii=False, indent=4)
print(node_json_str)
