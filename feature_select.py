#! /usr/bin/env python
#coding = utf-8
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def loadData_all(filename):
    fr = open(filename)
    dataMat = [];label = [];items = []
    context = fr.readlines()
    fr.close()
    for line in context:
        array = line.strip().split(',')
        items.append(array[0])
        array = [float(x) for x in array[1:]]
        dataMat.append((array[:-1]))
        label.append(array[-1])
    return dataMat, label, items


#Load boston housing dataset as an example
X = []
Y = []
Z = []
[X,Y,Z] = loadData_all('./data/lbj_st_all.csv')
names = ["STORE_CODE","CATE_ID",
	    "CATE_LEVEL_ID","BRAND_ID",
	    "SUPPLIER_ID","PV_IPV",
	    "PV_UV","CART_IPV",
	    "CART_UV","COLLECT_UV",
	    "NUM_GMV","AMT_GMV",
	    "QTY_GMV","UNUM_GMV",
	    "AMT_ALIPAY","NUM_APLIPAY",
	    "QTY_APIPAY","UNUM_ALIPAY",
	    "ZTC_PV_IPV","TBK_PV_IPV",
	    "SS_PV_IPV","JHS_PV_IPV",
	    "ZTC_PV_UV","TBK_PV_UV",
	    "SS_PV_UV","JHS_PV_UV",
	    "NUM_AIPAY_HJHS","AMT_APLIPAY_NJHS",
	    "QTY_ALIPAY_NJHS","UNUM_ALIPAY_NJHS",
	    "SALES3","SALES5",
	    "SALES7","SALES14",
	    "SALES30","SALES60","SALES90"]
rf = RandomForestRegressor()
rf.fit(X, Y)
feature_select =  sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_ ), names), reverse=True)
feature_selected = feature_select[:10]
feature_id=[]
for i in range(10):
	feature_id.append(names.index(feature_selected[i][1]))
print feature_id
print feature_selected


