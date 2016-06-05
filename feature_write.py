#! /usr/bin/env python
# coding = utf-8

feature_id = [32, 28, 21, 33, 27, 30, 17, 26, 7, 29]
#feature_id = [33, 31, 28, 29, 22, 18, 34, 7, 35, 8]

def loadData_all(filename):
    fr = open(filename)
    dataMat = [];label = [];items = []
    context = fr.readlines()
    fr.close()
    for line in context:  #从每行开始读
        array = line.strip().split(',')　
        items.append(array[0])
        array = [float(x) for x in array[1:]]　　 
        dataMat.append((array[:-1]))　#读取 除了第一列和最后一列
        label.append(array[-1])
    return dataMat, label, items

[X1,Y1,Z1] = loadData_all('./data/sub_DataSet1.csv') 
tmp = []
X1_tmp = []
for row in X1:
	for index in feature_id:
		tmp.append(row[index])
	X1_tmp.append(tmp)
	tmp = []

fp = open('./data/sub_DataSet_yc.csv','w')   #保存降维后的数据在　sub_DataSet_yc.csv

for i in range(len(X1_tmp)):
	fp.write('%s,'%Z1[i])  
	for j in range(len(X1_tmp[i])):
                if j != len(X1_tmp[i])-1:
                    fp.write('%s,'%X1_tmp[i][j])
                else:
                    fp.write('%s\n'%X1_tmp[i][j])
