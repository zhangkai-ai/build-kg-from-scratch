#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
@author  : Winnie
@contact : fyli.winnie@gmail.com
@description: 

'''
import re
import pandas as pd
from sklearn import model_selection

# NER标签定义
d = {
    'song': '-SO',
    'artist': '-AR',
    'genre': '-GE'
}

def sequence_label(sent, label):
    extract_labels = {}
    if 'song' in label:
        extract_labels['song'] = label['song']
    if 'artist' in label:
        extract_labels['artist'] = label['artist']
    if 'genre' in label:
        extract_labels['genre'] = label['genre']
    seq = len(sent) * ['O']
    matched_info = []
    if extract_labels:
        for k, v in extract_labels.items():
            mm = re.finditer(v, sent)
            for m in mm:
                matched_info.append([m.span(), k, v])

    # 下面一段代码是校验语料是否有不同标签标注重叠的
    # matched_info_sort = sorted(matched_info, key=lambda x:x[0][0])
    # right = 0
    # try:
    #     for p in matched_info_sort:
    #         assert right < p[0][1]
    #         right = p[0][1]
    # except:
    #     print('异常', sent)

    for m in matched_info:
        l = m[0][0]
        r = m[0][1]
        flag = d[m[1]]
        if r - l == 1:
            lab = ['S' + flag]
        elif r - l == 2:
            lab = ['B' + flag] + ['E' + flag]
        else:
            lab = ['B' + flag]+ (r-l-2)*['I'+ flag] + ['E' + flag]

        seq[l:r] = lab

    assert len(seq) == len(sent)
    return seq

def write_crf_format(filename, sents, seq_labels):
    with open(filename, 'w', encoding='utf8') as outfile:
        for sent,label in zip(sents, seq_labels):
            for s,l in zip(sent, label):
                outfile.write(s+'\t'+l+'\n')
            outfile.write('\n')


df = pd.read_csv('/Users/winnie/Desktop/music_ner.csv')
df['labels'] = df['labels'].map(lambda x: eval(x))
df['seq_label'] = df.apply(lambda x:sequence_label(x['sents'], x['labels']), axis=1)
df.to_csv('/Users/winnie/Desktop/music_ner_label.csv',index=False)
new_df = df.sample(frac=1).reset_index(drop=True)
# print(new_df)
sents = new_df['sents']
seq_labels = new_df['seq_label']


X_train, X_test, y_train, y_test = model_selection.train_test_split(sents,seq_labels, test_size=0.2)
write_crf_format('/Users/winnie/Desktop/music_ner_train.txt', X_train,y_train)
write_crf_format('/Users/winnie/Desktop/music_ner_test.txt', X_test,y_test)

# sent = '你好周杰伦，播放贼拉拉的爱你是一首情歌。'
# seq = len(sent) * ['O']
# label = {'song': '贼拉拉的爱你', 'artist': '周', 'genre': '情歌'}
# matched_info = []
# for k, v in label.items():
#     mm = re.finditer(v, sent)
#     for m in mm:
#         matched_info.append([m.span(), k, v])

#
# matched_info_sort = sorted(matched_info, key=lambda x:x[0][0])
#
# print(matched_info)
# d = {
#     'song': '-SO',
#     'artist': '-AR',
#     'genre': '-GE'
# }
# for m in matched_info:
#     l = m[0][0]
#     r = m[0][1]
#     flag = d[m[1]]
#     if r - l == 1:
#         lab = ['S' + flag]
#     elif r - l == 2:
#         lab = ['B' + flag] + ['E' + flag]
#     else:
#         lab = ['B' + flag]+ (r-l-2)*['I'+ flag] + ['E' + flag]
#
#     seq[l:r] = lab
#
# print(seq)