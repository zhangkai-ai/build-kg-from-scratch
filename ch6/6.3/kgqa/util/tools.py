#!/usr/bin/env python
# -*- coding:utf8 -*-

__author__ = 'winnie'

import re
import json
from collections import OrderedDict

class Utils():
    punc_ch = "[！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠《》｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…﹏]"
    punc_en = "[!\"#$%&\'()*+,;<=>?@[\\]^_`{|}~]"
    punc_ch_pattern = re.compile(punc_ch)
    punc_en_pattern = re.compile(punc_en)

    def __init__(self):
        pass

    def read_file_into_list(self, filename):
        line_list = []
        with open(filename, encoding='utf8') as infile:
            for line in infile:
                line = line.strip()
                if line:
                    line_list.append(line)
        return line_list

    def write_list_into_file(self, object, filename):
        with open(filename, 'w',encoding='utf8') as outfile:
            for line in object:
                outfile.write(line+'\n')

    def read_es(self,filename):
        ret_dict = OrderedDict()
        with open(filename) as infile:
            for line in infile:
                lineL = line.split('\t')
                if lineL[1] in ret_dict:
                    ret_dict[lineL[1]].append(lineL[2:])
                else:
                    ret_dict[lineL[1]] = [lineL[2:]]

        return ret_dict

    def write_dict_into_file_according_key(self, subject_dict, out_path):
        # 写入文件
        for key in subject_dict:
            with open(out_path+key+'.txt','wb', encoding='utf8') as outfile:
                for line in subject_dict[key]:
                    #print type(line),line
                    # if isinstance(line,unicode):
                    #     line = line.encode('utf8')
                    outfile.write(line+'\n')

    # dict的value是一个list
    def update_dict(self, origin_dict,new_dict):
        for key in new_dict:
            if key not in origin_dict:
                origin_dict[key] = new_dict[key]
            else:
                origin_dict[key].extend(new_dict[key])
        return origin_dict

    def remove_punctuation(self, sent):
        sent = self.punc_ch_pattern.sub('', sent)
        sent = self.punc_en_pattern.sub('', sent)
        # sent = re.sub(self.punc_ch_pattern, '', sent)
        # sent = re.sub(self.punc_en_pattern, '', sent)
        # sent = re.sub('[ ]{2,}', ' ', sent) # 去掉多余空格
        sent = ' '.join(sent.split())
        return sent

    def make_kg_mapping(self):
        json_file = 'hupo_kgqa/data/kg_mapping/amber-kg.json'
        with open(json_file, encoding='utf8') as infile:
            kg_dict = json.load(infile)
        for key in kg_dict:
            for ele in kg_dict[key]:
                print(ele)
            print()

    # def check_unicode(self, text):
    #     if isinstance(text,str):
    #         text = unicode(text,'utf8')
    #     elif isinstance(text, int) or isinstance(text, float):
    #         text = str(text)
    #
    #     return text

    # def read_json(self,filename):
         # with open(filename,) as infile:
         #    return json.load(infile)

    def json_dump(self, object, json_file):
        with open(json_file, 'w', encoding='utf8') as f:
            json.dump(object, f, indent=4, ensure_ascii=False)

    def read_json(self, json_file):
        with open(json_file, 'r', encoding='utf8') as f:
           structure = json.load(f)
        return structure



util = Utils()


#util.make_kg_mapping()

# 展示字典，二维
# raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
#         'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
#         'age': [42, 52, 36, 24, 73],
#         'preTestScore': [4, 24, 31, ".", "."],
#         'postTestScore': ["25,000", "94,000", 57, 62, 70]}
# df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
# print df
# 展示效果
#   first_name last_name  age preTestScore postTestScore
# 0      Jason    Miller   42            4        25,000
# 1      Molly  Jacobson   52           24        94,000
# 2       Tina         .   36           31            57
# 3       Jake    Milner   24            .            62
# 4        Amy     Cooze   73            .            70

# d1 = {'a':1,'b':2}
# d2 = {'a':2,'b':3}
# d3 = {'a':3,'b':1}
# l = [d1,d2,d3]
# l.sort(key=lambda e: e['a'],reverse=True)
# print l

