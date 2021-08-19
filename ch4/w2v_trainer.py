#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
词向量训练代码
词向量加载代码详见ch7/nlu/w2v_trainer.py
"""

import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


model = Word2Vec(LineSentence("w2v_corpus"),
                 size=300, window=10, min_count=5,
                 workers=multiprocessing.cpu_count())
model.save("w2v.model")
model.wv.save_word2vec_format("w2v.bin", binary=True)

