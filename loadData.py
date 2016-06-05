#!/usr/bin/env python
#coding=utf-8
'''
Created on 2016年4月20日
@author: wxquare
'''
###############################################################
# Load Nationwide data
def LoadData_DATA_LABEL_ITEM(filename):
    fr = open(filename)
    dataMat = [];label = [];items = []
    context = fr.readlines()
    for line in context:
        array = line.strip().split(',')
        items.append( array[0] )                    #first col is ITEM_ID
        array = [ float(x) for x in array[1:] ]
        dataMat.append( array[:-1] )
        label.append( array[-1] )                    #last col is  LABEL
    return dataMat, label, items


def LoadData_DATA_ITEM(filename):
    fr = open(filename)
    dataMat = [];items = []
    context = fr.readlines()
    for line in context:
        array = line.strip().split(',')
        items.append(array[0])                  #first col is ITEM_ID
        array = [float(x) for x in array[1:] ]
        dataMat.append(array)
    return dataMat, items


###############################################################
## Load the Sub-warehouse data 
def LoadData_DATA_ST(filename):
    fr = open(filename)
    dataMat = {}
    keys = ['1','2','3','4','5']
    for key in keys:
        dataMat[key]=[]
    context = fr.readlines()
    for line in context:
        array = line.strip().split(',')
        dataMat[array[1]].append(array)
    return dataMat

##############################################################################
# Load cost
def LoadCost(filename):
    print('loading cost...')
    cost_dict = {}
    cost_dict['all'] = {}
    cost_dict['1'] = {}
    cost_dict['2'] = {}
    cost_dict['3'] = {}
    cost_dict['4'] = {}
    cost_dict['5'] = {}
    fr = open(filename)
    context = fr.readlines()
    for line in context:
        array = line.strip('\n').split(',')
        cost_dict[array[1]][array[0]] = [ float(x) for x in (array[2].split('_')) ]
    return cost_dict

