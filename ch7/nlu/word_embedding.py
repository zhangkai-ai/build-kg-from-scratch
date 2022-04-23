#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
词向量
Tencent_AILab_ChineseEmbedding.txt
页面：https://ai.tencent.com/ailab/nlp/en/embedding.html
下载链接：https://ai.tencent.com/ailab/nlp/en/data/Tencent_AILab_ChineseEmbedding.tar.gz
使用的话，引用如下信息:
@InProceedings{N18-2028,
  author =      "Song, Yan
                and Shi, Shuming
                and Li, Jing
                and Zhang, Haisong",
  title =       "Directional Skip-Gram: Explicitly Distinguishing Left and Right Context for Word Embeddings",
  booktitle =   "Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)",
  year =        "2018",
  publisher =   "Association for Computational Linguistics",
  pages =       "175--180",
  location =    "New Orleans, Louisiana",
  url =         "http://aclweb.org/anthology/N18-2028"
}
"""

import numpy as np
from gensim.models import FastText
from nlu.seg.ltp_util import ltp_seg_handler
from gensim.models.keyedvectors import KeyedVectors

# 读者需要修改为自己存放词向量文件的路径，否则会报错！！！
PATH = '/Users/winnie/software_package/'
WORD_VECTOR = PATH + 'Tencent_AILab_ChineseEmbedding_Min.txt'


# print("Loading word vector...")
# word_vector = KeyedVectors.load_word2vec_format(WORD_VECTOR_PATH, binary=True)
# print("Loading word vector complete!")

def word_embeding_txt_to_bin():
    '''
    直接下载的词向量文件解压后是.txt格式的，加载缓慢，建议转为二进制.bin格式；
    加载完整词向量预计需要25分钟~30分钟，读者仅做实验的话，可以选取文件前10万行做一个精简版：Tencent_AILab_ChineseEmbedding_Min.txt；
    记得修改Tencent_AILab_ChineseEmbedding.txt文件的第一行"8824330 200"为"100000 200"，否则会报解析错误
    '''
    wv = KeyedVectors.load_word2vec_format(WORD_VECTOR, binary=False)
    # 以二进制格式保存
    wv.load_word2vec_format(PATH + 'Tencent_Embedding_Min.bin', binary=True)


def get_similarity(model, w1, w2):
    '''
    求w1和w2之间的相似度
    :param model: model为加载进内存的词向量模型
    :param w1: 第一个词
    :param w2: 第二个词
    :return:
    '''
    try:
        sim = model.wv.similarity(w1, w2)
    except Exception as e:
        print(e)
        sim = 0
    return sim

def euclidean_distance(model, w1, w2):
    # 欧式距离计算两个词相似度
    vec1 = model[w1]
    vec2 = model[w2]
    dis = np.sqrt(np.sum(np.square(vec1 - vec2)))
    return dis


def read_corpus(filename):
    '''
    读取语料并调用ltp分词工具
    :param filename:
    :return:
    '''
    sent_list = []
    with open(filename, 'r', encoding='utf8') as fp:
        for line in fp:
            sent_list.append(ltp_seg_handler.segment(line.strip()))
    return sent_list

def train_fasttext_embedding(corpus_file):
    '''
    训练fasttext基于ngram subword信息的词向量模型
    :param corpus_file: 输入语料文本数据
    :return:
    '''
    print('开始加载语料...')
    sentences = read_corpus(corpus_file)
    print('语料处理完开始训练...')
    model = FastText(sentences, size=200, window=5, min_count=2, min_n=1, max_n=5, workers=4, iter=5)
    model.save('fasttext_wv_model.bin')
    print('训练完成！')


if __name__ == "__main__":
    # 1、将.txt的词向量转为二进制格式
    # word_embeding_txt_to_bin()

    # 2、基于word2vec词向量获得词汇的向量
    # Tencent_Embedding_Min.bin为Tencent_AILab_ChineseEmbedding.txt前10万行的精简版二进制版本
    word_vector_path = PATH + 'Tencent_Embedding_Min.bin'
    model = KeyedVectors.load_word2vec_format(word_vector_path, binary=True)
    # 获取一个词的向量方式1
    print(model['中国'])  # 词向量获得的方式
    # 获取一个词的向量方式2
    print(model.wv['中国']) # 词向量获得的方式

    # 3、通过FastText训练词向量，解决未登录词的问题
    # 3.1 训练方法
    filename = '../data/corpus.txt'
    train_fasttext_embedding(filename)
    # 3.2 获取词汇FastText的词向量，该词可以是一个OOV词汇
    model = FastText.load('fasttext_wv_model.bin')
    # 获取一个OOV词的方式
    print(model.wv['奥利给222'])
    print(model['奥利给222'])
    # 输出最相近的词汇
    print(model.wv.most_similar("漂亮", topn=10))
    # 计算两个词的余弦相似度
    print(get_similarity(model, '漂亮', '好看'))
    # 计算两个词的欧氏距离
    print(euclidean_distance(model,'漂亮','好看'))

