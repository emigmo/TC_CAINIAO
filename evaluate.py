#!/usr/bin/env python
#coding=utf-8
import time
import GDBT_all
import GDBT_ST
import SVR as s
import RF
from sklearn.svm.classes import SVR


##############################################################################
# load cost
def loadCost():
    print('loading cost...')
    cost_dict = {}
    cost_dict['all'] = {}
    cost_dict['1'] = {}
    cost_dict['2'] = {}
    cost_dict['3'] = {}
    cost_dict['4'] = {}
    cost_dict['5'] = {}
    fr = open('./data/config1.csv')
    context = fr.readlines()
    for line in context:
        array = line.strip('\n').split(',')
        cost_dict[array[1]][array[0]] = [float(x) for x in (array[2].split('_'))]
    fr.close()
    return cost_dict
cost_dict = loadCost()


##############################################################################
#已当前日期命名文件
date = time.strftime('%Y%m%d')
filename = './data/' + 'sub' + date + '.csv'


##############################################################################
# 训练全国的数据
def train_all():
    RF_all1 = RF.RF_ALL_train('./data/testingDataSet1.csv', './data/VALIDATION_DataSet1.csv')
    RF_all2 = RF.RF_ALL_train('./data/EVAL_DataSet1.csv', './data/VALIDATION_DataSet1.csv')
    gdbt_all1 = GDBT_all.GDBT_ALL_train('./data/VALIDATION_DataSet1.csv', './data/VALIDATION_DataSet1.csv')
    gdbt_all2 = GDBT_all.GDBT_ALL_train('./data/testingDataSet1.csv', './data/VALIDATION_DataSet1.csv')
    gdbt_all3 = GDBT_all.GDBT_ALL_train('./data/EVAL_DataSet1.csv', './data/VALIDATION_DataSet1.csv')
    svr_all = s.SVR_ALL_train()
     
    # 3个GBDTt，1个sSVR再做一次SVR
    #     X = [];Y = []
    #     for i in range(len(gdbt_all1)):
    #         X.append((RF_all1[i][2], gdbt_all1[i][2], gdbt_all2[i][2], svr_all[i][2],svr_all[i][3]))
    #         Y.append(gdbt_all1[i][3])
    #          
    #     svr = SVR(kernel='linear', epsilon=2, C=1).fit(X, Y)
    #     print(svr.coef_)
    #     pred_y = svr.fit(X, Y).predict(X)
        
    fw = open(filename, 'w')
    for i in range(len(gdbt_all1)):
        fw.write('%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' % 
                 (gdbt_all1[i][0], gdbt_all1[i][1],
                  float(RF_all1[i][2]),
                  float(RF_all2[i][2]),
                  float(gdbt_all1[i][2]),
                  float(gdbt_all2[i][2]),
                  float(gdbt_all3[i][2]),
                  float(svr_all[i][2]),
                  float(svr_all[i][3]), #前14天的值
                  float(svr_all[i][4]),
                  ((float(RF_all1[i][2])+float(gdbt_all1[i][2]) + float(gdbt_all2[i][2])+ \
                        float(svr_all[i][2]) + float(svr_all[i][3])+float(svr_all[i][4]))) / 6,
                  cost_dict['all'][gdbt_all1[i][0]][0],
                  cost_dict['all'][gdbt_all1[i][0]][1],
                  float(gdbt_all1[i][3])
                  )
                 )
    
    fw.close()



##############################################################################
# 单独训练每个仓库
def train_ST():
    RF_st1 = RF.RF_ST_train('./data/testingDataSetST1.csv', './data/VALIDATION_DataSetST1.csv')
    RF_st2 = RF.RF_ST_train('./data/EVAL_DataSetST1.csv', './data/VALIDATION_DataSetST1.csv')
    gdbt_st1 = GDBT_ST.GDBT_ST_train('./data/EVAL_DataSetST1.csv', './data/VALIDATION_DataSetST1.csv')
    gdbt_st2 = GDBT_ST.GDBT_ST_train('./data/testingDataSetST1.csv', './data/VALIDATION_DataSetST1.csv')
    gdbt_st3 = GDBT_ST.GDBT_ST_train('./data/VALIDATION_DataSetST1.csv', './data/VALIDATION_DataSetST1.csv')
    svr_st = s.SVR_ST_train()
     
    #     # 3个GBDT，1个sSVR再做一次SVR
    #     store = ['1', '2', '3', '4', '5'];pred_y = []
    #     for st in store:
    #         X = [];Y = []
    #         for i in range(len(gdbt_st1)):
    #             if gdbt_st1[i][1] != st: continue
    #             X.append((RF_st1[i][2], gdbt_st1[i][2], gdbt_st2[i][2], svr_st[i][2]))
    #             Y.append(gdbt_st1[i][3])       
    #         svr = SVR(kernel='linear', epsilon=0.5, C=1).fit(X, Y)
    #         svr_res = svr.predict(X)
    #         for x in svr_res:
    #             pred_y.append(x)
    
    fw = open(filename, 'a')
    for i in range(len(gdbt_st1)):
        fw.write('%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' % 
                 (gdbt_st1[i][0], gdbt_st1[i][1],
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
                  float(gdbt_st1[i][3])
                  )
                 )
    fw.close()
    

#######################################################################################
# calculate cost 
if __name__ == '__main__':
    print('calculating cost...')
    for i in range(10):
        train_all()
        train_ST()
        fr = open(filename)
        cost =0;cost1 = 0;cost2 = 0;cost3 = 0;cost4 = 0;cost5 = 0;cost6 = 0;cost7 = 0
        cost_all=0;cost_all1 = 0;cost_all2 = 0;cost_all3 = 0;cost_all4 = 0;
        cost_all5 = 0;cost_all6 = 0;cost_all7 = 0
    
        context = fr.readlines()
        fr.close()
        for line in context:
            array = line.strip('\n').split(',')
            t = cost_dict[str(array[1])][array[0]]
            
            a =[]
            if t[0]<t[1]:
                a = [float(x) for x in array[3:11]]
                a.sort()
                diff = (a[0]+a[1]+a[2]+a[3])/4*0.85 - float(array[-1])
            else:
                a = [float(x) for x in array[3:11]]
                a.sort(reverse=True)
                diff = (a[0]+a[1]+a[2]+a[3])/4*1.15 - float(array[-1])
                
            diff1 = float(array[2]) - float(array[-1])
            diff2 = float(array[3]) - float(array[-1])
            diff3 = float(array[4]) - float(array[-1])
            diff4 = float(array[5]) - float(array[-1])
            diff5 = float(array[6]) - float(array[-1])
            diff6 = float(array[7]) - float(array[-1])
            diff7 = float(array[8]) - float(array[-1])
    
            #计算全部费用
            t = cost_dict[str(array[1])][array[0]]
            cost +=t[0] * max(0 - diff, 0) + t[1] * max(diff, 0)
            cost1 += t[0] * max(0 - diff1, 0) + t[1] * max(diff1, 0)
            cost2 += t[0] * max(0 - diff2, 0) + t[1] * max(diff2, 0)
            cost3 += t[0] * max(0 - diff3, 0) + t[1] * max(diff3, 0)
            cost4 += t[0] * max(0 - diff4, 0) + t[1] * max(diff4, 0)
            cost5 += t[0] * max(0 - diff5, 0) + t[1] * max(diff5, 0)
            cost6 += t[0] * max(0 - diff6, 0) + t[1] * max(diff6, 0)
            cost7 += t[0] * max(0 - diff7, 0) + t[1] * max(diff7, 0)
    
            # 计算全国的费用
            if array[1] != 'all': continue
            t = cost_dict['all'][array[0]]
            cost_all +=t[0] * max(0 - diff, 0) + t[1] * max(diff, 0)
            cost_all1 += t[0] * max(0 - diff1, 0) + t[1] * max(diff1, 0)
            cost_all2 += t[0] * max(0 - diff2, 0) + t[1] * max(diff2, 0)
            cost_all3 += t[0] * max(0 - diff3, 0) + t[1] * max(diff3, 0)
            cost_all4 += t[0] * max(0 - diff4, 0) + t[1] * max(diff4, 0)
            cost_all5 += t[0] * max(0 - diff5, 0) + t[1] * max(diff5, 0)
            cost_all6 += t[0] * max(0 - diff6, 0) + t[1] * max(diff6, 0)
            cost_all7 += t[0] * max(0 - diff7, 0) + t[1] * max(diff7, 0)
              
        print('全部成本：%d,%d,%d,%d,%d,%d,%d,%d' % \
              (int(cost1), int(cost2), int(cost3), int(cost4), int(cost5), int(cost6), int(cost7),int(cost)))
        print('全国成本：%d,%d,%d,%d,%d,%d,%d,%d' % \
              (int(cost_all1), int(cost_all2), int(cost_all3), int(cost_all4), \
                    int(cost_all5), int(cost_all6), int(cost_all7),int(cost_all)))

    
    
    
    
