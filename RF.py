#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月28日
@author: wxquare
'''
import loadData as ld
from sklearn.ensemble.forest import RandomForestRegressor

def RF_ALL(trainFileName,testFileName):
    train_X, train_y, _ = ld.LoadData_DATA_LABEL_ITEM(trainFileName)
    Eval_X, items = ld.LoadData_DATA_ITEM(testFileName)
    clf = RandomForestRegressor(n_estimators=100,criterion='mse', max_depth=None,max_features='auto',bootstrap=True).\
            fit(train_X, train_y)
    pred_y = clf.predict(Eval_X)
    res = []
    for i in range(len(Eval_X)):
        res.append([items[i],'all','%.4f'%max(pred_y[i],0)])
    return res


def RF_ST_train(trainFileName,testFileName):
    trainData = ld.loadData_ST(trainFileName)
    testData = ld.loadData_ST(testFileName)
    
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
         
        clf = RandomForestRegressor(criterion='mse', n_estimators=100, max_depth=None).\
                    fit(train_X,train_y)
        pred_y = clf.predict(test_X)
         
        for i in range(len(pred_y)):
            res.append([items[i][0],items[i][1],'%.2f'%max(pred_y[i],0),'%.2f'%max(test_y[i],0)])
    return res

def RF_ST(trainFileName,testFilename):
    trainData = ld.LoadData_DATA_ST(trainFileName)
    testData = ld.LoadData_DATA_ST(testFilename)
    
    store = ['1','2','3','4','5']
    res = []
    
    for i in store:
        train_X = [];train_y = []
        context = trainData[i]
        for array in context:
            array = [float(x) for x in array[2:]]
            train_X.append((array[2:-1]))
            train_y.append(array[-1])
            
        test_X = [];items = []
        context = testData[i]
        for array in context:
            items.append((array[0],array[1]))
            array = [float(x) for x in array[2:] ]
            test_X.append((array[2:]))
            
         
        clf = RandomForestRegressor(n_estimators=100,criterion='mse', max_depth=None,max_features='auto').\
                    fit(train_X,train_y)
        pred_y = clf.predict(test_X)
         
        for i in range(len(pred_y)):
            res.append([items[i][0],items[i][1],'%.4f'%max(pred_y[i],0)])
    return res
