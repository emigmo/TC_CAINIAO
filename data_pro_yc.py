#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Created on Thu May 12 13:50:22 2016
@author: yc
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

def process_all():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_all.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_all.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])
	return train,label

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_all.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_all.txt',label2,delimiter = ',')
def process_store1():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_1.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_1.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_1.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_1.txt',label2,delimiter = ',')
def process_store2():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_2.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_2.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_2.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_2.txt',label2,delimiter = ',')
def process_store3():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_3.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_3.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_3.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_3.txt',label2,delimiter = ',')
def process_store4():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_4.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_4.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_4.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_4.txt',label2,delimiter = ',')
def process_store5():
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
	    if len(a[item])>=period+after:  #针对每个Item 如果其记录超过28条。
	        number_item_big +=1
	        for i in range(len(a[item])-period-period-after)[::interval]:
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
	savetxt('./data/train_data_feature_5.txt',train,delimiter = ',')
	label = array(item_label)
	print ('train label data has: ' + str(label.shape))
	savetxt('./data/train_data_label_5.txt',label,delimiter = ',')

	#print(cross_validation.cross_val_score(linear_model.LinearRegression(),train,label).mean())
	#print(cross_validation.cross_val_score(svm.LinearSVR(),train,label).mean())
	#%%
	item_train2=[]
	item_label2=[]
	for item in a.keys():
	    if len(a[item])>period+after:
	        item_train2.append(a[item].iloc[-period-after:-after].mean(0))
	        item_label2.append([item,a[item].iloc[-after:]['qty_alipay_njhs'].mean(0)])
	    else:
	        item_train2.append(a[item].iloc[-int(0.5*len(a[item])):].mean(0))
	        item_label2.append([item,a[item].iloc[-int(0.5*len(a[item])):]['qty_alipay_njhs'].mean(0)])    

	train2 = array(item_train2)
	item_label2=DataFrame(item_label2)
	item_label2.columns=['item_id','label2']
	label2 = array(item_label2['label2'])

	print ('the test data has: ' + str(train2.shape))
	savetxt('./data/test_data_feature_5.txt',train2,delimiter = ',')
	print ('the test label data has:'+str(label2.shape))
	savetxt('./data/test_data_label_5.txt',label2,delimiter = ',')

if __name__=='__main__':
	process_all()
	process_store1()
	process_store2()
	process_store3()
	process_store4()
	process_store5()
