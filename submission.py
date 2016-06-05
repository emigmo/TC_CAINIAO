#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月19日
@author: wxquare
'''
import GDBT_all
import SVR as s
import time
import GDBT_ST
import RF
import loadData as ld

date = time.strftime('%Y%m%d')
submissionFilename = './data/'+'sub'+ date+'.csv'
tmpFilename = './data/tmp.csv'

def sub_all():
    print('training all...')
    RF_all1 = RF.RF_ALL('./data/Normalized_Data/testing_DataSet.csv', './data/Normalized_Data/sub_DataSet.csv')
    RF_all2 = RF.RF_ALL('./data/Normalized_Data/EVAL_DataSet.csv', './data/Normalized_Data/sub_DataSet.csv')
    gdbt_all1 = GDBT_all.GDBT_ALL('./data/Normalized_Data/training_DataSet.csv','./data/Normalized_Data/sub_DataSet.csv')
    gdbt_all2 = GDBT_all.GDBT_ALL('./data/Normalized_Data/testing_DataSet.csv','./data/Normalized_Data/sub_DataSet.csv')
    gdbt_all3 = GDBT_all.GDBT_ALL('./data/Normalized_Data/EVAL_DataSet.csv','./data/Normalized_Data/sub_DataSet.csv')
    svr_all = s.SVR_ALL('./data/Normalized_Data/EVAL_DataSet.csv', './data/Normalized_Data/sub_DataSet.csv')
    
    fw = open(tmpFilename,'w')
    for i in range(len(svr_all)):
        fw.write('%s,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' %
                (gdbt_all1[i][0],gdbt_all1[i][1],
                 float(RF_all1[i][2]),
                 float(RF_all2[i][2]),
                 float(gdbt_all1[i][2]),
                 float(gdbt_all2[i][2]),
                 float(gdbt_all3[i][2]),
                 float(svr_all[i][2]),
                 float(svr_all[i][3]),
                 float(svr_all[i][4]),
                ((float(RF_all2[i][2])+float(gdbt_all1[i][2]) + float(gdbt_all2[i][2])+\
                  float(svr_all[i][2]) + float(svr_all[i][3])+float(svr_all[i][4]))) / 6,
                cost_dict['all'][gdbt_all1[i][0]][0],
                cost_dict['all'][gdbt_all1[i][0]][1]
                ))
    fw.close()

def sub_st():
    print('training ST...')
    RF_st1 = RF.RF_ST('./data/Normalized_Data/testing_DataSetST.csv', './data/Normalized_Data/sub_DataSetST.csv')
    RF_st2 = RF.RF_ST('./data/Normalized_Data/EVAL_DataSetST.csv', './data/Normalized_Data/sub_DataSetST.csv')
    gdbt_st1 = GDBT_ST.GDBT_ST('./data/Normalized_Data/testing_DataSetST.csv','./data/Normalized_Data/sub_DataSetST.csv')
    gdbt_st2 = GDBT_ST.GDBT_ST('./data/Normalized_Data/EVAL_DataSetST.csv','./data/Normalized_Data/sub_DataSetST.csv')
    gdbt_st3 = GDBT_ST.GDBT_ST('./data/Normalized_Data/EVAL_DataSetST.csv','./data/Normalized_Data/sub_DataSetST.csv')
    svr_st = s.SVR_ST('./data/Normalized_Data/EVAL_DataSetST.csv','./data/Normalized_Data/sub_DataSetST.csv')
  
    fw = open(tmpFilename,'a')    #追加写入文件
    for i in range(len(svr_st)):

        fw.write('%s,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' %
                (gdbt_st1[i][0],gdbt_st1[i][1],
                 float(RF_st1[i][2]),
                 float(RF_st2[i][2]),
                 float(gdbt_st1[i][2]),
                 float(gdbt_st2[i][2]),
                 float(gdbt_st3[i][2]),
                 float(svr_st[i][2]),
                 float(svr_st[i][3]),
                 float(svr_st[i][4]),
                 (float(RF_st2[i][2])+float(gdbt_st1[i][2]) + float(gdbt_st2[i][2]) + \
                    float(svr_st[i][2])+float(svr_st[i][3])+float(svr_st[i][4])) / 6,
                  cost_dict[gdbt_st1[i][1]][gdbt_st1[i][0]][0],
                  cost_dict[gdbt_st1[i][1]][gdbt_st1[i][0]][1],
                  ))
    fw.close()
    
if __name__ == '__main__':
    cost_dict = ld.LoadCost('./data/config1.csv')
    sub_all()
    sub_st()
    fr = open(tmpFilename)
    context = fr.readlines()

    fw = open(submissionFilename,'w')
    for line in context:
        array = line.strip('\n').split(',')
        t = cost_dict[str(array[1])][array[0]]
        if t[0]<t[1]:
            a = [float(x) for x in array[3:11]]
            a.sort()
            diff = (a[0]+a[1]+a[2]+a[3])/4*0.9
        else:
            a = [float(x) for x in array[3:11]]
            a.sort(reverse=True)
            diff = (a[0]+a[1]+a[2]+a[3])/4*1.1
            
        fw.write('%s,%s,%.4f\n' %
                (array[0],array[1],
                 float(diff)
                 ))
    fw.close()
    print('finished!')
            
       














