#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Created on Thu May 12 13:50:22 2016
@author: yc
"""

fp = open('./item.name.csv')

line = fp.readlines().strip().split(',')
print line
