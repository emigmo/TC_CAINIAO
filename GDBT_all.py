#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月12日
@author: wxquare
'''
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
import numpy as np
import matplotlib.pyplot as plt
import loadData as ld


###############################################################
# fitting GDBT
def GDBT_ALL_train(trainFileName,testFileName):
    train_X, train_y, _ = ld.loadData_all(trainFileName)
    test_X, test_y,items = ld.loadData_all(testFileName)
    clf = GradientBoostingRegressor(loss='lad', n_estimators=40, learning_rate=0.1, max_depth=3).\
            fit(train_X, train_y)
    pred_y = clf.predict(test_X)
    res = []
    for i in range(len(test_X)):
        res.append([items[i],'all','%.2f'%max(pred_y[i],0),'%.2f'%max(test_y[i],0)])
    return res


def GDBT_ALL(trainFileName,testFileName):
    train_X, train_y, _ = ld.LoadData_DATA_LABEL_ITEM(trainFileName)
    Eval_X, items = ld.LoadData_DATA_ITEM(testFileName)
    clf = GradientBoostingRegressor(loss='lad', n_estimators=40, learning_rate=0.1, max_depth=3).\
            fit(train_X, train_y)
    pred_y = clf.predict(Eval_X)
    res = []
    for i in range(len(Eval_X)):
        res.append([items[i],'all','%.4f'%max(pred_y[i],0)])
    return res
#############################################################
# Plot training deviance
# find the best arguments
if __name__ == '__main__':
    
    train_X, train_y, _ = ld.loadData_all('./data/SQL_Result/testingDataSet.csv')
    test_X, test_y,items = ld.loadData_all('./data/SQL_Result/VALIDATION_DataSet.csv')
#     clf = GradientBoostingRegressor(loss='lad', n_estimators=40, learning_rate=0.1, max_depth=3).\
#             fit(train_X, train_y)
#     pred_y = clf.predict(test_X)
    print('trainging...')
    
#     trainData = ld.loadData_ST('./data/EVAL_DataSetST1.csv')
#     testData = ld.loadData_ST('./data/trainingDataSetST1.csv')
#     
#     store = ['1','2','3','4','5']
#     res = []
#     
#   
#     i = store[4]
#     train_X = [];train_y = []
#     context = trainData[i]
#     for array in context:
#         array = [float(x) for x in array[2:] ]
#         train_X.append((array[2:-1]))
#         train_y.append(array[-1])
#     test_X = [];test_y = [];items = []
#     context = testData[i]
#     for array in context:
#         items.append((array[0],array[1]))
#         array = [float(x) for x in array[2:] ]
#         test_X.append((array[2:-1]))
#         test_y.append(array[-1])
                        
    n_etemators = 1000
    clf1 = GradientBoostingRegressor(loss='lad', n_estimators=n_etemators, learning_rate=0.01, max_depth=3,verbose=0).\
            fit(train_X, train_y)
    test_score1 = np.zeros((n_etemators,), dtype=np.float64)
    for i, pred_y in enumerate(clf1.staged_predict(test_X)):
        print(i,clf1.feature_importances_)
        test_score1[i] = clf1.loss_(test_y, pred_y)
    
#     clf2 = GradientBoostingRegressor(loss='lad', n_estimators=n_etemators, learning_rate=0.1, max_depth=2,verbose=0).\
#             fit(train_X, train_y)
#     test_score2 = np.zeros((n_etemators,), dtype=np.float64)
#     for i, pred_y in enumerate(clf2.staged_predict(test_X)):
#         test_score2[i] = clf2.loss_(test_y, pred_y)
#     
#     clf3 = GradientBoostingRegressor(loss='lad', n_estimators=n_etemators, learning_rate=0.1, max_depth=2,verbose=0,subsample=0.5).\
#             fit(train_X, train_y)
#     test_score3 = np.zeros((n_etemators,), dtype=np.float64)
#     for i, pred_y in enumerate(clf3.staged_predict(test_X)):
#         test_score3[i] = clf2.loss_(test_y, pred_y)
    
    plt.figure()
    plt.title('testing-VALIDATION Deviance')
    plt.plot(np.arange(n_etemators) + 1, clf1.train_score_, 'b-', label='Training Set Deviance')
    
    plt.plot(np.arange(n_etemators) + 1, test_score1, 'r-', label='testing Set Deviance')
#     plt.plot(np.arange(n_etemators) + 1, test_score2, 'orange', label='testing Set Deviance')
#     plt.plot(np.arange(n_etemators) + 1, test_score3, 'gray', label='testing Set Deviance')
    
    plt.legend(loc='upper right')
    plt.xlabel('Boosting Iterations')
    plt.ylabel('Deviance')  
    plt.show()





