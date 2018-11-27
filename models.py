#!/usr/bin/env python

from __future__ import print_function
from scipy.io import loadmat
import numpy as np
import csv
import math
from sklearn.model_selection import train_test_split 
import re
from scipy.sparse import csc_matrix
from os import listdir
from os.path import isfile,join

def estimate_naive_bayes_classifier(X,Y):# X: data Y: labels
    #raise Exception("IMPLEMENT ME")
    d = len(X.toarray()[0])
    y = np.unique(Y).shape[0]
    row = X.shape[0]
    
    params = {}
    params['pi'] = np.array([0] * y, dtype='float64')
    params['mu'] = np.array([[0] * d] * y, dtype='float64')
    for i in range(y):
        label = i + 1
        indices = Y == label
        cur_X = X[indices,:]
        params['pi'][i] = cur_X.shape[0] / row
        params['mu'][i] = (1 + np.sum(cur_X,axis = 0)) / (2 + cur_X.shape[0])
    return params
         
def predict(params,X):
    res = np.array([0] * X.shape[0])
    part1 = np.log(params['pi'] * np.prod(1 - params['mu'],axis = 1))
    part1 = np.tile(part1, (X.shape[0],1)).transpose()
    part2 = np.log(params['mu'] / (1 - params['mu']))
    part2 = part2.dot(X.toarray().transpose())
    res = part1 + part2
    res = np.argmax(res,axis = 0) + 1
    return res

def print_top_words(params,vocab):
    part2 = np.log(params['mu'] / (1 - params['mu']))
    a = part2[1] - part2[0]
    sort_a = np.argsort(a)
    neg = sort_a[:20]
    pos = sort_a[-20:]
    pos_vocab = []
    neg_vocab = []
    for i in range(20):
        pos_vocab.append(vocab[pos[i]])
    for i in range(20):
        neg_vocab.append(vocab[neg[i]])
    print('top postive 20 words:',pos_vocab)
    print('top negtive 20 words:',neg_vocab)
    #raise Exception("IMPLEMENT ME")
    return 

def load_data():
    data = []
    labels = []
    categories = ['tech','business','entertainment','politics','sport']
    for category in categories:
        mypath = join('./bbc',category)
        for f in listdir(mypath):
            try:
                row = []
                #print(join(mypath, f))
                text = open(join(mypath, f))
                tem = text.read()
                words = re.split(r'(\W)',tem)
                for word in words:
                    if len(word) > 0 and word[0].isalpha():
                        row.append(word)
                data.append(row)
                labels.append(category)
                text.close()
            except:
                pass
            
    return (data,labels)

def construct_dic(text):
    log_idf = {}
    dic = {}
    mapping = {}
    mapping['affine parameter'] = 0
    log_idf['affine parameter'] = 0
    pos = 1
    for row in text:
        for word in row:
            if word in dic.keys():
                dic[word] += 1
            else:
                mapping[word] = pos
                dic[word] = 1
                pos += 1
    D = len(text)
    for item in dic.items():
        log_idf[item[0]] = math.log10(D / item[1])
    return (log_idf,mapping)            

def tokenize(data,labels,mapping):
    labels_mapping = {'tech':0,'business':1,'entertainment':2,'politics':3,'sport':4}
    n = len(labels)
    d = len(mapping)
    x = np.zeros((n,d), dtype='int')
    y = np.zeros(n, dtype='int')
    #print(x.shape,y.shape)
    for i in range(n):
        y[i] = labels_mapping[labels[i]]+1
        for j in range(len(data[i])):
            #print(i,j,mapping[data[i][j]])
            x[i][mapping[data[i][j]]] = 1
    return (csc_matrix(x),y)

def transform(test_data,mapping):
    res = np.array([0] * len(mapping))
    words = re.split(r'(\W)',test_data)
    for word in words:
        if word in mapping.keys():
            res[mapping[word]] = 1
    return csc_matrix(res)
        

def load_vocab():
    with open('news.vocab') as f:
        vocab = [ x.strip() for x in f.readlines() ]
    return vocab

if __name__ == '__main__': 
    (data,labels) = load_data()
    log_idf,mapping = construct_dic(data)
    data,labels = tokenize(data,labels,mapping)
    X_train, X_val, y_train, y_val =train_test_split(data, labels, test_size=0.2, random_state=1)
    params1 = estimate_naive_bayes_classifier(X_train,y_train)
    pred = predict(params1,X_train) # predictions on training data
    val_pred = predict(params1,X_val) # predictions on test data
    np.save('model.npy', params1) 
    #read_dictionary = np.load('model.npy').item()
    #print('training error rate: %g' % np.mean(pred != y_train))
    #print('test error rate: %g' % np.mean(val_pred != y_val))
