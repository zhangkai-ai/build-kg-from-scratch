#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
ltp分词、NER、依存句法分析
注意，该代码适用于pyltp 0.4.0新版本，安装的是0.2.x版本的同学请移步ltp_util.py，两个版本对应的python封装不一致，
pyltp 0.4.0更多调用示例参考：https://github.com/HIT-SCIR/pyltp/blob/master/example/example.py
# 详细的ltp标签说明文档： https://ltp.readthedocs.io/zh_CN/latest/appendix.html
# 模型下载网盘地址：随便选一个版本下载即可，不需要全部下载
# https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569&errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=#list/path=%2Fltp-models
"""

import os
from pyltp import Segmentor
from pyltp import CustomizedSegmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller

# 请下载任意一个版本的LTP模型，修改下方LTP_PATH的值再使用，否则路径会报错！！（百度网盘的下载链接在第7行）
LTP_PATH = '/Users/winnie/software/ltp_data_v3.4.0/'

class LTPHander():

    def __init__(self, ltp_path, task_type='seg', seg_dict=''):
        '''
        task_type可选：
        - seg       分词
        - postag    词性标注
        - ner       命名实体识别
        - parser    依存分析
        - semantic  语义角色标注
        :param ltp_path: ltp模型存放的路径
        :param task_type: 任务的类型
        '''
        self.LTP_DATA_DIR = ltp_path
        # 分词，默认加载
        self._cws_model_path = os.path.join(self.LTP_DATA_DIR,'cws.model') # 分词模型路径，模型名称`cws.model`

        if seg_dict: # 引入用户字典分词模式
            # 两种模式供选择使用
            # self._segmentor = Segmentor(self._cws_model_path, lexicon_path=seg_dict)  # 分开的会合并在一起
            self._segmentor = Segmentor(self._cws_model_path, force_lexicon_path=seg_dict)  # 除上述功能外，原本合并在一起的亦会拆分
        else:
            self._segmentor = Segmentor(self._cws_model_path)

        # 词性标注，默认加载
        self._pos_model_path = os.path.join(self.LTP_DATA_DIR, 'pos.model') # 词性标注模型路径，模型名称为`pos.model`
        self._postagger = Postagger(self._pos_model_path)

        if task_type == 'ner': # NER
            self._ner_model_path = os.path.join(self.LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
            self._ner = NamedEntityRecognizer(self._ner_model_path) # 初始化实例

        if task_type == 'parser':# 依存分析
            self._par_model_path = os.path.join(self.LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
            self._parser = Parser(self._par_model_path) # 初始化实例

        if task_type == 'semantic': # 语义角色标注
            self._par_model_path = os.path.join(self.LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
            self._parser = Parser(self._par_model_path) # 初始化实例
            self._srl_model_path = os.path.join(self.LTP_DATA_DIR, 'pisrl.model')
            self._labeller = SementicRoleLabeller(self._srl_model_path) # 初始化实例

    def segment(self, sent):
        # 分词方法
        words = self._segmentor.segment(sent)
        return list(words)

    def pos_tag(self, sent):
        # 词性标注方法
        words = self.segment(sent)
        postags = self._postagger.postag(words)
        return list(postags)

    def ner(self, sent):
        '''
        NER方法，共可以识别三种类型的命名实体：
        - Nh	人名
        - Ni	机构名
        - Ns	地名
        :param sent: 中国工商银行总部在哪里
        :return: [(0, 6, '中国工商银行', 'Ni')]
                 [(开始index, 结束index, NE子串1, NE类型), (开始index, 结束index, NE子串2, NE类型), ……]
        '''
        words = self.segment(sent)  # 分词结果
        postags = self.pos_tag(sent)  # 词性标注结果
        netags = self._ner.recognize(words, postags)
        res = []
        cur_index = 0
        ne_start = 0  # 实体开始的词的index
        start = 0  # 实体开始的下标位置
        for i, lab in enumerate(netags):
            # 当ner标签为O和I的时候，跳到下一个词，更新cur_index
            if netags[i] == 'O' or netags[i].startswith('I'):
                cur_index += len(words[i])
                continue
            # 当标签为S时，表示单个词成实体
            if netags[i].startswith('S'):
                start = cur_index
                end = cur_index + len(words[i])
                ne_type = netags[i].split('-')[1]
                ne_words = words[i]
                res.append((start, end, ne_words, ne_type))
            # 当标签为B时，表示该词是实体开头的词
            elif netags[i].startswith('B'):
                ne_start = i
                start = cur_index
            # 当标签为E时，表示该词是实体结束的词
            elif netags[i].startswith('E'):
                ne_end = i
                end = cur_index + len(words[i])
                ne_type = netags[i].split('-')[1]
                ne_words = ''.join(words[ne_start:ne_end + 1])
                res.append((start, end, ne_words, ne_type))
            cur_index += len(words[i])

        return res

    def parser(self, sent):
        '''
        Root节点索引为0，第一个词开始索引为1、2、3……
        arcs每个元素是tuple格式(head, relation)，head 表示依存弧的父节点词的索引，relation 表示依存弧的关系
        :param sent: 输入句子
        :return: [(head父节点逻辑序号, 父节点词, 当前词逻辑序号, 当前词, relation关系),  ……]
        '''
        words = self.segment(sent)
        postags = self.pos_tag(sent)
        arcs = self._parser.parse(words, postags)  # 句法分析
        # 打印结果
        print("\t".join("%d:%s" % (head, relation) for (head, relation) in arcs))
        parser_words = ['ROOT'] + words
        res = [(head, parser_words[head], idx+1, parser_words[idx+1], relation) for idx, (head, relation) in enumerate(arcs)]

        return res

    def semantic_labeller(self, sent):
        '''
        第一个词开始的索引依次为0、1、2……
        index 代表谓词的索引，
        arguments 代表关于该谓词的若干语义角色。
        arguments中的name 表示语义角色类型
        arguments中的start 表示该语义角色起始词位置的索引，
        arguments中的end 表示该语义角色结束词位置的索引。

        :param sent:
        :return: [(谓词1下标, 谓词1, [(name, start, end, 对应字符串), (name, start, end, 对应字符串), ……]),
                  (谓词2下标, 谓词2, [(name, start, end, 对应字符串), (name, start, end, 对应字符串), ……]),
                  (……, ……, ……)]
        '''
        words = self.segment(sent)
        postags = self.pos_tag(sent)
        arcs = self._parser.parse(words, postags)  # 句法分析
        roles = self._labeller.label(words, postags, arcs)  # 语义角色标注

        res = []
        for index, arguments in roles:
            args = [(name, start, end, ''.join(words[start:end+1])) for (name, (start, end)) in arguments]
            res.append((index, words[index], args))

        # 打印结果
        for index, arguments in roles:
            print(index, " ".join(["%s: (%d,%d)" % (name, start, end) for (name, (start, end)) in arguments]))

        return res


ltp_seg_handler = LTPHander(LTP_PATH, task_type='seg')


if __name__ == '__main__':
    # sent = '告白气球是周杰伦的歌吗？'
    sent = '中国工商银行在北京的总部地址，周杰伦的告白气球，市长江大桥，小明喜欢小红'
    noun_candidate_set = set()
    # 默认分词模型
    ltp = LTPHander(LTP_PATH, task_type='seg')
    print(ltp.segment(sent))
    # 加载用户自定义词表分词
    ltp = LTPHander(LTP_PATH, task_type='seg', seg_dict='pyltp_user_dict.txt')
    print(ltp.segment(sent))
    # 词性标注
    ltp = LTPHander(LTP_PATH, task_type='postag')
    print(ltp.pos_tag(sent))
    # NER
    ltp = LTPHander(LTP_PATH, task_type='ner')
    print(ltp.ner(sent))
    # 依存分析
    ltp = LTPHander(LTP_PATH, task_type='parser')
    print('parser:',ltp.parser(sent))
    # 语义角色标注
    ltp = LTPHander(LTP_PATH, task_type='semantic')
    print(ltp.semantic_labeller(sent))

