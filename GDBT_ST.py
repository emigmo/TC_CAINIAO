#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月12日
@author: wxquare
'''
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
import loadData as ld


def GDBT_ST_train(trainFileName,testFileName):
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
         
        clf = GradientBoostingRegressor(loss='lad', n_estimators=50, learning_rate=0.1, max_depth=3).\
                    fit(train_X,train_y)
        pred_y = clf.predict(test_X)
         
        for i in range(len(pred_y)):
            res.append([items[i][0],items[i][1],'%.2f'%max(pred_y[i],0),'%.2f'%max(test_y[i],0)])
    return res

###############################################################
# fitting GDBT
def GDBT_ST(trainFileName,testFilename):
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
            
        clf = GradientBoostingRegressor(loss='lad', n_estimators=50, learning_rate=0.1, max_depth=3).\
                    fit(train_X,train_y)
        pred_y = clf.predict(test_X)
         
        for i in range(len(pred_y)):
            res.append([items[i][0],items[i][1],'%.4f'%max(pred_y[i],0)])
    return res








