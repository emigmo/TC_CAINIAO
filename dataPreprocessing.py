#coding=utf-8
'''
Created on 2016年4月21日
@author: wxquare
'''
import math

###############################################
#########Preprocess the Nationwide Store###############
#[ITEM_ID],[ ]*29,[SALES3],[SALES5],[SALES7],[SALES14],[SALES30],[SALES60],[SALES90],[LABEL]
    #trainingDataSet.csv
    #testingDataSet.csv
    #EVAL_DataSet.csv
    #VALIDATION_DataSet.csv
    #sub_DataSet.csv
 def Data_Preprocessing_all(inputfilename,outputfilename):
    fw = open(outputfilename,'w')
    fr  = open(inputfilename,'r')
    context = fr.readlines()
    for line in context[1:]:                   #first col is the ITEM_ID
        array = line.strip('\n').split(',')
        for i in range( len(array) - 1 ):  
            array[i+1] ='%.4f' % math.log10( 1+float( array[i+1] ) )  #Feature Normalize
        for i in range(len(array)):
            if i != (len(array)-1): 
                fw.write('%s,'%(array[i]))
            else:
                fw.write('%s\n'%array[i])       
    print( "Preprocessed the : "+ inputfilename)    

def Data_Preprocessing_all_NO_LABEL(inputfilename,outputfilename):
    fw = open(outputfilename,'w')
    fr  = open(inputfilename,'r')
    context = fr.readlines()
    for line in context[1:]:                   #first col is the ITEM_ID
        array = line.strip('\n').split(',')
        for i in range( len(array) - 2 ):  
            array[i+1] ='%.4f' % math.log10( 1+float( array[i+1] ) )  #Feature Normalize
        for i in range(len(array)):
            if i != (len(array)-1): 
                fw.write('%s,'%(array[i]))
            else:
                fw.write('%s\n'%array[i])       
    print( "Preprocessed the : "+ inputfilename) 
###############################################
#########Preprocess the Sub-warehouse Store###############
#[ITEM_ID],[STORE_CODE],[ ]*29,[SALES3],[SALES5],[SALES7],[SALES14],[SALES30],[SALES60],[SALES90],[LABEL]
    #trainingDataSet.csv
    #testingDataSet.csv
    #EVAL_DataSet.csv
    #VALIDATION_DataSet.csv
    #sub_DataSet.csv
def Data_Preprocessing_ST(inputfilename,outputfilename):
    fw = open(outputfilename,'w')
    fr  = open(inputfilename,'r')
    context = fr.readlines()
    for line in context[1:]:            #first row is the Tag from the SQL
        array = line.strip('\n').split(',')
        for i in range( len(array) - 2 ):  
            array[i+2] ='%.4f' % math.log10( 1+float( array[i+2] ) )  #Feature Normalize
        for i in range(len(array)):
            if i != (len(array)-1): 
                fw.write('%s,'%(array[i]))
            else:
                fw.write('%s\n'%array[i])       
    print( "Preprocessed the : "+ inputfilename)

def Data_Preprocessing_ST_NO_LABEL(inputfilename,outputfilename):
    fw = open(outputfilename,'w')
    fr  = open(inputfilename,'r')
    context = fr.readlines()
    for line in context[1:]:            #first row is the Tag from the SQL
        array = line.strip('\n').split(',')
        for i in range( len(array) - 3 ):  
            array[i+2] ='%.4f' % math.log10( 1+float( array[i+2] ) )  #Feature Normalize
        for i in range(len(array)):
            if i != (len(array)-1): 
                fw.write('%s,'%(array[i]))
            else:
                fw.write('%s\n'%array[i])       
    print( "Preprocessed the : "+ inputfilename)


if __name__ == '__main__':
    print ("Preprocessing Nationwide Data...")
    Data_Preprocessing_all('./data/SQL_Result/EVAL_DataSet.csv','./data/Normalized_Data/EVAL_DataSet.csv')
    Data_Preprocessing_all('./data/SQL_Result/training_DataSet.csv','./data/Normalized_Data/training_DataSet.csv')
    Data_Preprocessing_all('./data/SQL_Result/testing_DataSet.csv','./data/Normalized_Data/testing_DataSet.csv')
    Data_Preprocessing_all('./data/SQL_Result/VALIDATION_DataSet.csv','./data/Normalized_Data/VALIDATION_DataSet.csv')
    Data_Preprocessing_all_NO_LABEL('./data/SQL_Result/sub_DataSet.csv','./data/Normalized_Data/sub_DataSet.csv')

    print ("Preprocessing Sub-warehouse Data...")
    Data_Preprocessing_ST('./data/SQL_Result/EVAL_DataSetST.csv','./data/Normalized_Data/EVAL_DataSetST.csv')
    Data_Preprocessing_ST('./data/SQL_Result/training_DataSetST.csv','./data/Normalized_Data/training_DataSetST.csv')
    Data_Preprocessing_ST('./data/SQL_Result/testing_DataSetST.csv','./data/Normalized_Data/testing_DataSetST.csv')
    Data_Preprocessing_ST('./data/SQL_Result/VALIDATION_DataSetST.csv','./data/Normalized_Data/VALIDATION_DataSetST.csv')
    Data_Preprocessing_ST_NO_LABEL('./data/SQL_Result/sub_DataSetST.csv','./data/Normalized_Data/sub_DataSetST.csv')

    
    