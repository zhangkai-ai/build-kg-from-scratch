#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
词向量
Tencent_ChineseEmbedding.bin
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
from seg.ltp_util import ltp_seg_handler
from gensim.models.keyedvectors import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from numpy import add, dot
from gensim import matutils


WORD_VECTOR_PATH = '/Users/winnie/software_package/Tencent_AILab_ChineseEmbedding.txt'


# print("Loading word vector...")
# word_vector = KeyedVectors.load_word2vec_format(WORD_VECTOR_PATH, binary=True)
# print("Loading word vector complete!")

def word_embeding_txt_to_bin():
    # 直接下载的词向量文件解压后是.txt格式的，加载缓慢，建议转为二进制.bin格式
    # 通常加载需要25分钟~30分钟
    wv = KeyedVectors.load_word2vec_format(WORD_VECTOR_PATH, binary=False)
    wv.load_word2vec_format('/Users/winnie/software_package/Tencent_AILab_ChineseEmbedding.bin', binary=True)


# def calcu_semantic_sim_split(word_a, word_b):
#     # word输入必须是utf8的str类型, ltp需要是str类型，word_vector需要是unicode类型
#     if type(word_a) == str:
#         word_a = word_a.decode('utf-8')
#     if type(word_b) == str:
#         word_b = word_b.decode('utf-8')
#
#     word_a_vec = []
#     if word_a in word_vector.vocab:
#         word_a_vec = word_vector.get_vector(word_a)
#     else:
#         seg_list = ltp_seg_handler.segment(word_a.encode('utf-8'))
#         for seg_part in seg_list:
#             seg_part = seg_part.decode('utf-8')
#             if seg_part in word_vector.vocab:
#                 if type(word_a_vec) == list:
#                     word_a_vec = word_vector.get_vector(seg_part)
#                 else:
#                     word_a_vec = add(word_a_vec, word_vector.get_vector(seg_part))
#         if type(word_a_vec) == list:
#             return -1
#     word_b_vec = []
#     if word_b in word_vector.vocab:
#         word_b_vec = word_vector.get_vector(word_b)
#     else:
#         seg_list = ltp_seg_handler.segment(word_b.encode('utf-8'))
#         for seg_part in seg_list:
#             seg_part = seg_part.decode('utf-8')
#             if seg_part in word_vector.vocab:
#                 if type(word_b_vec) == list:
#                     word_b_vec = word_vector.get_vector(seg_part)
#                 else:
#                     word_b_vec = add(word_b_vec, word_vector.get_vector(seg_part))
#         if type(word_b_vec) == list:
#             return -1
#
#     similarity = dot(matutils.unitvec(word_a_vec), matutils.unitvec(word_b_vec))
#     return similarity


# def get_similarity(word_a, word_b):
#     '''
#     :param word_a:
#     :param word_b:
#     :return: similarity num
#     '''
#     if type(word_a) == str:
#         word_a = word_a.decode('utf-8')
#     if type(word_b) == str:
#         word_b = word_b.decode('utf-8')
#     similarity = 0
#     try:
#         similarity = word_vector.similarity(word_a, word_b)
#     except Exception as e:
#         # print(e)
#         pass
#     return similarity


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
    dis = np.sqrt(np.sum(np.square(vec1-vec2)))
    return dis


from gensim.models import FastText

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
    sentences = read_corpus(corpus_file)
    model = FastText(sentences, size=200, window=5, min_count=2, min_n=1, max_n=5, workers=4, iter=5)
    model.save('fasttext_wv_model.bin')

    # 模型加载
    model = FastText.load('fasttext_wv_model.bin')
    # 获取一个词的向量方式1
    print(model['中国'])  # 词向量获得的方式
    # 获取一个词的向量方式2
    print(model.wv['中国']) # 词向量获得的方式
    # 获取一个OOV词的方式
    print(model.wv['奥利给222'])
    print(model['奥利给222'])

    print(model.wv.most_similar("漂亮", topn=10))



    # print(get_similarity(model, '漂亮', '好看'))

    # print(euclidean_distance(model,'漂亮','丑'))
    # print(model.wv['奥利给'])



if __name__ == "__main__":
    # word_embeding_txt_to_bin()
    filename = '/Users/winnie/work/project/my_code/sentence_feature/corpus.txt'

    # 模型加载
    model = FastText.load('ft_wv.bin')
    # 获取一个词的向量方式1
    print(model['中国'])  # 词向量获得的方式
    # 获取一个词的向量方式2
    print(model.wv['中国']) # 词向量获得的方式
    # 获取一个OOV词向量的方式
    print(model['奥利给222'])
    print(model.wv['奥利给222'])
    # 获取一个词最相近的topn个词
    print(model.wv.most_similar("漂亮", topn=10))
    # 计算两个词的相似度
    print(get_similarity(model, '漂亮', '丑'))
    print(euclidean_distance(model,'漂亮','美丽'))

    wv = KeyedVectors.load_word2vec_format(WORD_VECTOR_PATH, binary=False)
    # 获取一个词的向量方式1
    print(model['中国'])
    # 获取一个词的向量方式2
    print(model.wv['中国'])
    # train_fasttext_embedding(filename)
    # print(sentences[:10])

    # similarity = get_similarity('妻子', '老婆')
    # print(similarity)
    # while True:
    #     word_a = raw_input("请输入a:")
    #     word_b = raw_input("请输入b:")
    #     if type(word_a) == str:
    #         word_a = word_a.decode('utf-8')
    #     if type(word_b) == str:
    #         word_b = word_b.decode('utf-8')
    #     rst = get_similarity(word_a, word_b)
    #     print(rst)
    #     disambiguation_start_time = time.time()
    #     print('disambiguation cost: {}'.format(time.time() - disambiguation_start_time))
    # while True:
    #     word_a = input("请输入a:")
    #     if type(word_a) == str:
    #         word_a = word_a.decode('utf-8')
    #     start_time = time.time()
    #     rst = word_vector.get_vector(word_a)
    #     print('get vector cost: {}'.format(time.time() - start_time))

