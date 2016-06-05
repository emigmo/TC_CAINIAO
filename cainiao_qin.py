#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Created on Thu May 12 13:50:22 2016
@author: mlamp
"""

from pandas import *
from numpy import *
from sklearn import *
from xgboost import *

import numpy as np

col_name_item=read_csv('item.name.csv',sep='\t',delimiter=',')
col_item = list(col_name_item.columns.values)
col_name_store=read_csv('store.name.csv',sep='\t',delimiter=',')
col_store = list(col_name_store.columns.values)

t_item=read_csv( './data/CAINIAO_Part_II_Data_20160509/item_feature2.csv',sep='\t',delimiter=',',names=col_item,na_values=['(null)'],\
    dtype={'date':object,'item_id':int,'cate_id':int,'cate_level_id':int,'brand_id':int,'supplier_id':int} )
t_store=read_csv('./data/CAINIAO_Part_II_Data_20160509/item_store_feature2.csv',sep='\t',delimiter=',',names=col_store,na_values=['(null)'])

t_config=read_csv('./data/CAINIAO_Part_II_Data_20160509/config2.csv',sep='\t',delimiter=',',names=['item_id','store_code','a_b'],na_values=['(null)'])
def process_all(t_item):
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, 'all'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, 'all'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
def process_ST1(t_store):
    t_item = t_store[t_store['store_code']==1]
    del t_item['store_code']
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, '1'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, '1'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
def process_ST2(t_store):
    t_item = t_store[t_store['store_code']==2]
    del t_item['store_code']
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, '2'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, '2'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
def process_ST3(t_store):
    t_item = t_store[t_store['store_code']==3]
    del t_item['store_code']
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, '3'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, '3'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
def process_ST4(t_store):
    t_item = t_store[t_store['store_code']==4]
    del t_item['store_code']
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, '4'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, '4'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
def process_ST5(t_store):
    t_item = t_store[t_store['store_code']==5]
    del t_item['store_code']
    a={}
    for x in t_item['item_id'].unique():  #遍历所有的ITEM　每个ITEM 对应一个k_v
        a[x]=t_item[t_item['item_id']==x].sort_values(by='date')  #相同ITEM按照date排序
    #%%
    item_train=[]
    item_label=[]
    period=14
    after=14
    interval=1

    number_item_big = 0
    number_item_smell = 0

    for item in a.keys():
        if len(a[item])>=(period+after):  #针对每个Item 如果其记录超过28条。
            number_item_big +=1
            for i in range(len(a[item])-period-after)[::interval]:
                item_train.append(a[item].iloc[i:period+i].mean(0))
                item_label.append(a[item].iloc[period+i:period+i+after]['qty_alipay_njhs'].mean())
        else:#针对每个Item 如果其记录低于28条。
            number_item_smell +=1
            item_train.append(a[item].iloc[:int(0.5*len(a[item]))].mean(0))
            item_label.append(a[item].iloc[int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0))
    print ('record is bigger than 28 in one item have:'+str(number_item_big))
    print ('record is smeller than 28 in one item have:'+str(number_item_smell))

    train = array(item_train)
    print ('train data has: ' + str(train.shape))

    label = array(item_label)
    print ('train label data has: ' + str(label.shape))


    #print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
    #print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
    #%%
    item_train2=[]
    item_label2=[]
    for item in a.keys():
        if len(a[item])>=(period+after):
            item_train2.append(a[item].iloc[-after:].mean(0))
            item_label2.append([item, '5'])
        else:
            item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
            item_label2.append([item, '5'])    

    train2 = array(item_train2)

    item_label2=DataFrame(item_label2)
    item_label2.columns=['item_id','store_code']

    return train,label,train2,item_label2
#train,label,train2,item_label2 = process_all(t_item)
#train,label,train2,item_label2 = process_ST1(t_store)
#train,label,train2,item_label2 = process_ST2(t_store)
#train,label,train2,item_label2 = process_ST3(t_store)
#train,label,train2,item_label2 = process_ST4(t_store)
train,label,train2,item_label2 = process_ST5(t_store)

#model and train-->test

clf=XGBRegressor(15,0.1,500)
#clf=svm.LinearSVR()
#clf=linear_model.LinearRegression()
model=clf.fit(train,label)
predict2 = clf.predict(train2)
predict2=Series(predict2,name='predict2')

df=concat([item_label2,predict2],axis=1)

df.to_csv(r'./data/submission0515.txt', header=None, index=None, sep=',', mode='a')


