#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
@author  : Winnie
@contact : fyli.winnie@gmail.com
@description:

'''

import CRFPP

class MusicNER():
    '''
    用CRF++做音乐歌曲名、歌手名、曲风实体识别
    '''
    def __init__(self):
        self.crf_model = './data/model_music_ner'
        self.tagger = CRFPP.Tagger("-m " + self.crf_model)

    def ner_predict(self, sent):
        '''
        程序入口，预测一个句子的音乐实体
        :param sent: 输入一个句子
        :return: 返回匹配到的实体列表
        '''
        sent = sent.replace(' ', '')  # 去空字符
        self.tagger.clear()  # 清空标注器
        a = [self.tagger.add((w)) for w in sent]  # 将句子按char添加入标注器中
        self.tagger.parse()
        size = self.tagger.size()
        xsize = self.tagger.xsize()
        entity_list = []
        entity = ''
        start = 0
        label = ''
        # 记录标注结果
        for i in range(0, size):
            for j in range(0, xsize):
                char = self.tagger.x(i, j)
                tag = self.tagger.y2(i)
                if tag.startswith('B'):
                    entity += char
                    start = i
                    label = tag.split('-')[1]
                elif tag.startswith('I'):
                    entity += char
                elif tag.startswith('E'):
                    entity += char
                    entity_list.append((entity, start, label))
                    entity = ''
                elif tag.startswith('S'):
                    start = i
                    label = tag.split('-')[1]
                    entity_list.append((char, start, label))
                    entity = ''

        return entity_list

    def crf_format_to_plain(self, filename, col):
        '''
        将crf预测的列状格式文本转化为按行的文本
        :param filename: 输入crf预测的文本
        :param col:
        :return:
        '''
        sent_list = []
        sent = []
        with open(filename, encoding='utf8') as infile:
            for line in infile:
                line = line.rstrip()
                if line:
                    sent.append(line.split('\t')[col])
                else:
                    sent_list.append(''.join(sent))
                    sent = []
        return sent_list


def tidy_crf_format(filename, col):
    '''
    将crf_test命令预测出的文件中匹配到的实体提取返回
    :param filename: crf_test预测文本
    :param col: 序列标注的列号，0为文本，1为true_label，2为predict_label
    :return: 返回匹配到的实体
    '''
    matched = []
    one = [0, -1, '', '']  # 行号、开始位置、实体字符串list、实体标签
    line_num = 0  # 记录行号
    index = 0  # 记录当前字符在句子中的下标
    with open(filename, encoding='utf8') as infile:
        for line in infile:
            line = line.rstrip()  # 仅去掉右端的空格和换行
            if line:
                combo = line.split('\t')
                ch = combo[0]
                tag = combo[col]
                if tag.startswith('B'):  # 表一个实体的开始
                    one[0] = line_num  # 实体所属行号
                    one[1] = index  # 开始位置
                    one[2] += ch  # 当前字符添加到实体字符串
                    one[3] = tag.split('-')[1]  # 添加实体标签
                elif tag.startswith('I'):  # 实体中间，实体字符串添加当前字符
                    one[2] += ch
                elif tag.startswith('E'):  # 实体结束
                    one[2] += ch
                    matched.append(one)
                    one = [0, -1, [], '']  # 刷新one
                elif tag.startswith('S'):  # 即是实体开始又是实体结束
                    one[0] = line_num
                    one[1] = index  # 开始位置
                    one[2] += ch
                    one[3] = tag.split('-')[1]
                    matched.append(one)
                    one = [0, -1, '', '']
                index += 1
            else:
                index = 0
                line_num += 1

    return matched

def compute_p_r_f1(y_true, y_pred):
    '''
    计算序列标注结果的PRF值
    '''
    y_true = [str(e) for e in y_true]
    y_pred = [str(e) for e in y_pred]
    p = len(set(y_true).intersection(y_pred)) / len(y_pred)
    r = len(set(y_true).intersection(y_pred)) / len(y_true)
    f1 = 2 * p * r / (p + r)
    return p, r, f1

def evaluate_entity(y_true, y_pred):
    '''
    评测模型每类实体预测的PRF值
    '''
    so_true = list(filter(lambda x: x[3] == 'SO', y_true))
    ar_true = list(filter(lambda x: x[3] == 'AR', y_true))
    ge_true = list(filter(lambda x: x[3] == 'GE', y_true))

    so_pred = list(filter(lambda x: x[3] == 'SO', y_pred))
    ar_pred = list(filter(lambda x: x[3] == 'AR', y_pred))
    ge_pred = list(filter(lambda x: x[3] == 'GE', y_pred))

    so_p, so_r, so_f1 = compute_p_r_f1(so_true, so_pred)
    ar_p, ar_r, ar_f1 = compute_p_r_f1(ar_true, ar_pred)
    ge_p, ge_r, ge_f1 = compute_p_r_f1(ge_true, ge_pred)

    print('歌曲：', so_p, so_r, so_f1)
    print('歌手：', ar_p, ar_r, ar_f1)
    print('曲风：', ge_p, ge_r, ge_f1)


if __name__ == '__main__':
    music_ner = MusicNER()
    # 1. 模型预测
    print(music_ner.ner_predict('我想听邓紫棋的喜欢你'))

    # 2. 评测模型
    y_true = tidy_crf_format('./data/music_ner_test_predict.txt',1)
    y_pred = tidy_crf_format('./data/music_ner_test_predict.txt',2)
    evaluate_entity(y_true, y_pred)


