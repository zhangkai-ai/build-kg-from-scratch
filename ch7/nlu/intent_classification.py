#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
意图识别分类器
"""
import pandas as pd
import fasttext as ft
from fasttext import train_supervised
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def params_pool():
    """
    参数池，设置参数池
    :return: 返回多组参数的list
    """
    keys = ['lr', 'epoch', 'wordNgrams', 'dim', 'minCount', 'minn', 'maxn', 'bucket', 'loss', 'pretrainedVectors']
    params_setting_list = [
        [0.3, 20, 4, 300, 10, 1, 3, 500000, 'softmax'],
        [0.3, 10, 4, 300, 10, 1, 3, 500000, 'softmax'],
        [0.1, 10, 4, 300, 10, 1, 3, 500000, 'softmax'],
    ]
    params_list = [dict(zip(keys, values)) for values in params_setting_list]
    return params_list


def train_data_format(X, y, label='__label__'):
    """
    :param X: 训练数据[type:list]
    :param y: 训练数据的标签[type:list]
    """
    data_set = []
    for sent, lab in zip(X, y):
        try:
            data_set.append(label + str(lab) + ' ' + sent)
        except:
            print(sent, lab)
    return data_set


def split_sent_and_label(filename):
    # 拆分带标签的数据为句子列表和标签列表
    sents, labels = [], []
    with open(filename, encoding='utf8') as infile:
        for line in infile:
            line = line.strip()
            label, sent = line.split(' ', 1)
            label = label.replace('__label__', '')
            sents.append(sent)
            labels.append(label)

    return sents, labels


def write_list_into_file(object, filename):
    with open(filename, 'w', encoding='utf8') as outfile:
        for line in object:
            outfile.write(line + '\n')


def dataset_split(data_file):
    """
    拆分train_data、dev_data和test_data
    :param data_file:
    :return:
    """
    df = pd.read_excel(data_file)
    X = df['sent_cut'].tolist()  # 分好词的句子
    y = df['label'].tolist()
    # 拆分训练、测试、验证集
    X_train_dev, X_test, y_train_dev, y_test = train_test_split(X, y, test_size=0.2)
    X_train, X_dev, y_train, y_dev = train_test_split(X_train_dev, y_train_dev, test_size=0.2)
    # 将训练数据与标签组装
    train_data = train_data_format(X_train, y_train)
    test_data = train_data_format(X_test, y_test)
    dev_data = train_data_format(X_dev, y_dev)
    # 写入文件
    write_list_into_file(train_data, '../data/train_data.txt')
    write_list_into_file(test_data, '../data/test_data.txt')
    write_list_into_file(dev_data, '../data/dev_data.txt')


def fasttext_train(train_data, test_data, model_path, **kwargs):
    """
    训练模型、测试和输出各意图PRF值
    :param train_data: 训练数据.txt文件
    :param test_data: 测试数据.txt文件
    :param model_path: 保存模型的名称
    :param kwargs: 训练参数列表
    :return: 无
    """
    # 训练
    clf = train_supervised(input=train_data, **kwargs)
    clf.save_model('%s.bin' % model_path)
    # 测试
    result = clf.test(test_data)
    precision = result[1]
    recall = result[2]
    print('Precision: {0}, Recall: {1}\n'.format(precision, recall))
    # 输出每类PRF值
    test_sents, y_true = split_sent_and_label(test_data)
    y_pred = [i[0].replace('__label__', '') for i in clf.predict(test_sents)[0]]
    print(classification_report(y_true, y_pred, digits=3))


def test(test_file, model_path):
    # 测试模型并输出各类意图的PRF值
    clf = ft.load_model(model_path)
    test_sents, y_true = split_sent_and_label(test_file)
    y_pred = [i[0].replace('__label__', '') for i in clf.predict(test_sents)[0]]
    # 输出各类标签的PRF值
    print(classification_report(y_true, y_pred, digits=3))


def predict(sent_list, model_path, topN=3):
    # 预测句子list的结果
    clf = ft.load_model(model_path)
    # 预测结果
    res = clf.predict(sent_list, k=topN)
    # 预测标签
    y_pred = [[lab.replace('__label__', '') for lab in labs] for labs in res[0]]
    # 预测概率
    y_prob = [[p for p in probs] for probs in res[1] ]
    # 组装topN的预测结果
    topN_pred = list(zip(y_pred,y_prob))
    return topN_pred


if __name__ == '__main__':
    data = '../data/intent_data.xlsx'
    # 拆分训练测试验证集
    # dataset_split(data)
    # 设置参数
    kwargs = {'lr': 0.4, 'epoch': 10, 'wordNgrams': 4, 'dim': 300, 'minCount': 10, 'minn': 1, 'maxn': 3,
              'bucket': 500000, 'loss': 'softmax'}
    # 训练模型
    fasttext_train('../data/train_data.txt', '../data/dev_data.txt', 'model', **kwargs)
    # 测试模型
    # test('test_data.txt', 'model.bin')
    sent = ['你好 ， 你 在 干什么','姚明 身高 是 多少']
    print(predict(sent,'model.bin'))
    # clf = ft.load_model('model.bin')
    # print(clf.predict([sent], k=3))
