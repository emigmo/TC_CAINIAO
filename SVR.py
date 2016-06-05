#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月12日
@author: Administrator
'''
import numpy as np
from sklearn.svm.classes import SVR

import loadData as ld

def SVR_ALL_train():
    train_X,train_y,_= ld.loadData_all('./data/EVAL_DataSet1.csv')
    test_X,test_y,items = ld.loadData_all('./data/VALIDATION_DataSet1.csv')
    train_X=np.matrix(train_X)
    test_X = np.matrix(test_X)
    svr= SVR(kernel='linear',epsilon=0.5,C=1)
    pred_y=svr.fit(train_X[:,-8:-1], train_y).predict(test_X[:,-8:-1])
    res =[]
    for i in range(len(test_X)):
        res.append([items[i],'all','%.2f'%max(pred_y[i],0),'%.2f'%test_X[i,-4],'%.2f'%(float(test_X[i,-5])*2)])
    return res
def SVR_ST_train():
    trainData = ld.loadData_ST('./data/EVAL_DataSetST1.csv')
    testData = ld.loadData_ST('./data/VALIDATION_DataSetST1.csv')

    store = ['1','2','3','4','5']
    res = []
    for i in store:
        train_X = [];train_y = []
        context = trainData[i]
        for array in context:
            array = [float(x) for x in array[2:] ]
            train_X.append((array[2:-1]))
            train_y.append(array[-1])
        
        test_X = [];test_y = [];items = []
        context = testData[i]
        for array in context:
            items.append((array[0],array[1]))
            array = [float(x) for x in array[2:] ]
            test_X.append((array[2:-1]))
            test_y.append(array[-1])
        
        train_X=np.matrix(train_X)
        test_X = np.matrix(test_X)
        svr= SVR(kernel='linear',epsilon=0.5,C=1)
        pred_y=svr.fit(train_X[:,-8:-1], train_y).predict(test_X[:,-8:-1])
        for i in range(len(test_X)):
            res.append([items[i][0],items[i][1],'%.2f'%max(pred_y[i],0),'%.2f'%max(test_X[i,-4],0),'%.2f'%max(2*test_X[i,-5],0)])
    return res


def SVR_ALL(trainFileName,testFileName):
    train_X,train_y,_= ld.LoadData_DATA_LABEL_ITEM(trainFileName)
    test_X,items= ld.LoadData_DATA_ITEM(testFileName)
    train_X=np.matrix(train_X)
    test_X = np.matrix(test_X)
    svr= SVR(kernel='linear',epsilon=0.5,C=1)
    pred_y=svr.fit(train_X[:,-8:-3], train_y).predict(test_X[:,-7:-2])
    res =[]
    for i in range(len(test_X)):
        res.append([items[i],'all','%.4f'%max(pred_y[i],0),'%.4f'%test_X[i,-4],'%.4f'%(float(test_X[i,-5])*2)])
    return res

def SVR_ST(trainFileName,testFileName):
    trainData = ld.LoadData_DATA_ST(trainFileName)
    testData = ld.LoadData_DATA_ST(testFileName)
    
    store = ['1','2','3','4','5']
    res = []
    for i in store:
        train_X = [];train_y = []
        context = trainData[i]
        for array in context:
            array = [float(x) for x in array[2:] ]
            train_X.append((array[2:-1]))
            train_y.append(array[-1])
        
        test_X = [];items = []
        context = testData[i]
        for array in context:
            items.append((array[0],array[1]))
            array = [float(x) for x in array[2:] ]
            test_X.append((array[2:]))
            
        train_X=np.matrix(train_X)
        test_X = np.matrix(test_X)
        svr= SVR(kernel='linear',epsilon=0.5,C=1)
        pred_y=svr.fit(train_X[:,-8:-3], train_y).predict(test_X[:,-7:-2])
        for i in range(len(test_X)):
            res.append([items[i][0],items[i][1],'%.4f'%max(pred_y[i],0),'%.4f'%test_X[i,-4],'%.4f'%(float(test_X[i,-5])*2)])
    return res

