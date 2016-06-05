
-- 提取预测之前3,5,7,14,30,60,90的销量情况
-- 销量统计的是非聚划算的支付件数,qty_alipay_njhs
-- 由于商品并不是每天都有记录信息，先取平均，在乘以天数，大概估计总的销量情况
-- 生成表格TC_SALES_FEATURE

-- ------------------------------------------------------
-- FOR TRAINING
DROP TABLE TC_SALES_FEATURE_TRAIN_ST;
CREATE TABLE TC_SALES_FEATURE_TRAIN_ST AS
SELECT T90.ITEM_ID,T90.STORE_CODE,
  ROUND(T3.SALES*3/T3.RECORDS,2) AS SALES3,
  ROUND(T5.SALES*5/T5.RECORDS,2) AS SALES5,
  ROUND(T7.SALES*7/T7.RECORDS,2) AS SALES7,
  ROUND(T14.SALES*14/T14.RECORDS,2) AS SALES14,
  ROUND(T30.SALES*30/T30.RECORDS,2) AS SALES30,
  ROUND(T60.SALES*60/T60.RECORDS,2) AS SALES60,
  ROUND(T90.SALES*90/T90.RECORDS,2) AS SALES90
FROM
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST
    WHERE TIME>='20141121' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T90
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
    WHERE TIME>='20141221' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T60
ON T90.ITEM_ID = T60.ITEM_ID AND T90.STORE_CODE = T60.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
    WHERE TIME>='20150120' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T30
ON T90.ITEM_ID = T30.ITEM_ID AND T90.STORE_CODE = T30.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
    WHERE TIME>='20150205' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T14
ON T90.ITEM_ID = T14.ITEM_ID AND T90.STORE_CODE = T14.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
    WHERE TIME>='20150212' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T7
ON T90.ITEM_ID = T7.ITEM_ID AND T90.STORE_CODE = T7.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
   WHERE TIME>='20150214' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T5
ON T90.ITEM_ID  = T5.ITEM_ID AND T90.STORE_CODE = T5.STORE_CODE
LEFT JOIN
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TRAIN_20141121_0304_ST 
    WHERE TIME>='20150216' AND TIME <='20150218' GROUP BY ITEM_ID,STORE_CODE
)T3
ON T90.ITEM_ID = T3.ITEM_ID AND T90.STORE_CODE = T3.STORE_CODE;

-- 用平均值填补null
UPDATE TC_SALES_FEATURE_TRAIN_ST SET SALES60 = ROUND(SALES90*60/90,2) WHERE SALES60 IS NULL;
UPDATE TC_SALES_FEATURE_TRAIN_ST SET SALES30 = ROUND((SALES90*30/90+SALES60*30/60)/2,2) WHERE SALES30 IS NULL;
UPDATE TC_SALES_FEATURE_TRAIN_ST SET SALES14 = ROUND((SALES90*14/90+SALES60*14/60+SALES30*14/30)/3,2) WHERE SALES14 IS NULL;
UPDATE TC_SALES_FEATURE_TRAIN_ST SET SALES7 = ROUND((SALES90*7/90+SALES60*7/60+SALES30*7/30+SALES14*7/14)/4,2) WHERE SALES7 IS NULL;
UPDATE TC_SALES_FEATURE_TRAIN_ST SET SALES5 = ROUND((SALES90*5/90+SALES60*5/60+SALES30*5/30+SALES14*5/14+SALES7*5/7)/5,2) WHERE SALES5 IS NULL;
UPDATE TC_SALES_FEATURE_TRAIN_ST SET 
  SALES3 = ROUND((SALES90*3/90+SALES60*3/60+SALES30*3/30+SALES14*3/14+SALES7*3/7+SALES5*3/5)/6,2) WHERE SALES3 IS NULL;


-- -----------------------------------------------------------------
-- FOR TESTING

DROP TABLE TC_SALES_FEATURE_TEST_ST;
CREATE TABLE TC_SALES_FEATURE_TEST_ST AS
SELECT T90.ITEM_ID,T90.STORE_CODE,
  ROUND(T3.SALES*3/T3.RECORDS,2) AS SALES3,
  ROUND(T5.SALES*5/T5.RECORDS,2) AS SALES5,
  ROUND(T7.SALES*7/T7.RECORDS,2) AS SALES7,
  ROUND(T14.SALES*14/T14.RECORDS,2) AS SALES14,
  ROUND(T30.SALES*30/T30.RECORDS,2) AS SALES30,
  ROUND(T60.SALES*60/T60.RECORDS,2) AS SALES60,
  ROUND(T90.SALES*90/T90.RECORDS,2) AS SALES90
FROM
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150305' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T90
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150404' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T60
ON T90.ITEM_ID = T60.ITEM_ID AND T90.STORE_CODE = T60.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150504' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T30
ON T90.ITEM_ID = T30.ITEM_ID AND T90.STORE_CODE = T30.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150520' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T14
ON T90.ITEM_ID = T14.ITEM_ID AND T90.STORE_CODE = T14.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150527' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T7
ON T90.ITEM_ID = T7.ITEM_ID AND T90.STORE_CODE = T7.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150529' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T5
ON T90.ITEM_ID  = T5.ITEM_ID AND T90.STORE_CODE = T5.STORE_CODE
LEFT JOIN
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_TEST_20150305_0616_ST 
    WHERE TIME>='20150531' AND TIME <='20150602' GROUP BY ITEM_ID,STORE_CODE
)T3
ON T90.ITEM_ID = T3.ITEM_ID AND T90.STORE_CODE = T3.STORE_CODE;


-- 用平均值填补null
UPDATE TC_SALES_FEATURE_TEST_ST SET SALES60 = ROUND(SALES90*60/90,2) WHERE SALES60 IS NULL;
UPDATE TC_SALES_FEATURE_TEST_ST SET SALES30 = ROUND((SALES90*30/90+SALES60*30/60)/2,2) WHERE SALES30 IS NULL;
UPDATE TC_SALES_FEATURE_TEST_ST SET SALES14 = ROUND((SALES90*14/90+SALES60*14/60+SALES30*14/30)/3,2) WHERE SALES14 IS NULL;
UPDATE TC_SALES_FEATURE_TEST_ST SET SALES7 = ROUND((SALES90*7/90+SALES60*7/60+SALES30*7/30+SALES14*7/14)/4,2) WHERE SALES7 IS NULL;
UPDATE TC_SALES_FEATURE_TEST_ST SET SALES5 = ROUND((SALES90*5/90+SALES60*5/60+SALES30*5/30+SALES14*5/14+SALES7*5/7)/5,2) WHERE SALES5 IS NULL;
UPDATE TC_SALES_FEATURE_TEST_ST SET 
  SALES3 = ROUND((SALES90*3/90+SALES60*3/60+SALES30*3/30+SALES14*3/14+SALES7*3/7+SALES5*3/5)/6,2) WHERE SALES3 IS NULL;



-------------------------------------------------------------------------------------------------------------------------------
-- FOR EVALUATING
DROP TABLE TC_SALES_FEATURE_EVAL_ST;
CREATE TABLE TC_SALES_FEATURE_EVAL_ST AS
SELECT T90.ITEM_ID,T90.STORE_CODE,
  ROUND(T3.SALES*3/T3.RECORDS,2) AS SALES3,
  ROUND(T5.SALES*5/T5.RECORDS,2) AS SALES5,
  ROUND(T7.SALES*7/T7.RECORDS,2) AS SALES7,
  ROUND(T14.SALES*14/T14.RECORDS,2) AS SALES14,
  ROUND(T30.SALES*30/T30.RECORDS,2) AS SALES30,
  ROUND(T60.SALES*60/T60.RECORDS,2) AS SALES60,
  ROUND(T90.SALES*90/T90.RECORDS,2) AS SALES90
FROM
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150617' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T90
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150717' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T60
ON T90.ITEM_ID = T60.ITEM_ID AND T90.STORE_CODE= T60.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150816' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T30
ON T90.ITEM_ID = T30.ITEM_ID AND T90.STORE_CODE= T30.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150901' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T14
ON T90.ITEM_ID = T14.ITEM_ID AND T90.STORE_CODE= T14.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150908' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T7
ON T90.ITEM_ID = T7.ITEM_ID AND T90.STORE_CODE = T7.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150910' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T5
ON T90.ITEM_ID = T5.ITEM_ID AND T90.STORE_CODE = T5.STORE_CODE
LEFT JOIN
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_EVAL_20150617_0928_ST 
    WHERE TIME>='20150912' AND TIME <='20150914' GROUP BY ITEM_ID,STORE_CODE
)T3
ON T90.ITEM_ID = T3.ITEM_ID AND T90.STORE_CODE = T3.STORE_CODE;


-- 用平均值填补null
UPDATE TC_SALES_FEATURE_EVAL_ST SET SALES60 = ROUND(SALES90*60/90,2) WHERE SALES60 IS NULL;
UPDATE TC_SALES_FEATURE_EVAL_ST SET SALES30 = ROUND((SALES90*30/90+SALES60*30/60)/2,2) WHERE SALES30 IS NULL;
UPDATE TC_SALES_FEATURE_EVAL_ST SET SALES14 = ROUND((SALES90*14/90+SALES60*14/60+SALES30*14/30)/3,2) WHERE SALES14 IS NULL;
UPDATE TC_SALES_FEATURE_EVAL_ST SET SALES7 = ROUND((SALES90*7/90+SALES60*7/60+SALES30*7/30+SALES14*7/14)/4,2) WHERE SALES7 IS NULL;
UPDATE TC_SALES_FEATURE_EVAL_ST SET SALES5 = ROUND((SALES90*5/90+SALES60*5/60+SALES30*5/30+SALES14*5/14+SALES7*5/7)/5,2) WHERE SALES5 IS NULL;
UPDATE TC_SALES_FEATURE_EVAL_ST SET 
  SALES3 = ROUND((SALES90*3/90+SALES60*3/60+SALES30*3/30+SALES14*3/14+SALES7*3/7+SALES5*3/5)/6,2) WHERE SALES3 IS NULL;

-------------------------------------------------------------------------------------------------------------------------------
-- FOR SUBMISSION
DROP TABLE TC_SALES_FEATURE_SUB_ST;
CREATE TABLE TC_SALES_FEATURE_SUB_ST AS
SELECT T90.ITEM_ID,T90.STORE_CODE,
  ROUND(T3.SALES*3/T3.RECORDS,2) AS SALES3,
  ROUND(T5.SALES*5/T5.RECORDS,2) AS SALES5,
  ROUND(T7.SALES*7/T7.RECORDS,2) AS SALES7,
  ROUND(T14.SALES*14/T14.RECORDS,2) AS SALES14,
  ROUND(T30.SALES*30/T30.RECORDS,2) AS SALES30,
  ROUND(T60.SALES*60/T60.RECORDS,2) AS SALES60,
  ROUND(T90.SALES*90/T90.RECORDS,2) AS SALES90
FROM
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20150929' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T90
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151029' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T60
ON T90.ITEM_ID = T60.ITEM_ID AND T90.STORE_CODE= T60.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151128' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T30
ON T90.ITEM_ID = T30.ITEM_ID AND T90.STORE_CODE= T30.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151214' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T14
ON T90.ITEM_ID = T14.ITEM_ID AND T90.STORE_CODE= T14.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151221' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T7
ON T90.ITEM_ID = T7.ITEM_ID AND T90.STORE_CODE = T7.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151223' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T5
ON T90.ITEM_ID = T5.ITEM_ID AND T90.STORE_CODE = T5.STORE_CODE
LEFT JOIN
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_SUB_20150929_1227_ST 
    WHERE TIME>='20151225' AND TIME <='20151227' GROUP BY ITEM_ID,STORE_CODE
)T3
ON T90.ITEM_ID = T3.ITEM_ID AND T90.STORE_CODE = T3.STORE_CODE;


-- 用平均值填补null
UPDATE TC_SALES_FEATURE_SUB_ST SET SALES60 = ROUND(SALES90*60/90,2) WHERE SALES60 IS NULL;
UPDATE TC_SALES_FEATURE_SUB_ST SET SALES30 = ROUND((SALES90*30/90+SALES60*30/60)/2,2) WHERE SALES30 IS NULL;
UPDATE TC_SALES_FEATURE_SUB_ST SET SALES14 = ROUND((SALES90*14/90+SALES60*14/60+SALES30*14/30)/3,2) WHERE SALES14 IS NULL;
UPDATE TC_SALES_FEATURE_SUB_ST SET SALES7 = ROUND((SALES90*7/90+SALES60*7/60+SALES30*7/30+SALES14*7/14)/4,2) WHERE SALES7 IS NULL;
UPDATE TC_SALES_FEATURE_SUB_ST SET SALES5 = ROUND((SALES90*5/90+SALES60*5/60+SALES30*5/30+SALES14*5/14+SALES7*5/7)/5,2) WHERE SALES5 IS NULL;
UPDATE TC_SALES_FEATURE_SUB_ST SET 
  SALES3 = ROUND((SALES90*3/90+SALES60*3/60+SALES30*3/30+SALES14*3/14+SALES7*3/7+SALES5*3/5)/6,2) WHERE SALES3 IS NULL;




-------------------------------------------------------------------------------------------------------------------------------
-- FOR VALIDATION
DROP TABLE TC_SALES_FEATURE_VALIDAT_ST;
CREATE TABLE TC_SALES_FEATURE_VALIDAT_ST AS
SELECT T90.ITEM_ID,T90.STORE_CODE,
  ROUND(T3.SALES*3/T3.RECORDS,2) AS SALES3,
  ROUND(T5.SALES*5/T5.RECORDS,2) AS SALES5,
  ROUND(T7.SALES*7/T7.RECORDS,2) AS SALES7,
  ROUND(T14.SALES*14/T14.RECORDS,2) AS SALES14,
  ROUND(T30.SALES*30/T30.RECORDS,2) AS SALES30,
  ROUND(T60.SALES*60/T60.RECORDS,2) AS SALES60,
  ROUND(T90.SALES*60/T90.RECORDS,2) AS SALES90
FROM
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151015' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T90
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151015' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T60
ON T90.ITEM_ID = T60.ITEM_ID AND T90.STORE_CODE= T60.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151114' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T30
ON T90.ITEM_ID = T30.ITEM_ID AND T90.STORE_CODE= T30.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151130' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T14
ON T90.ITEM_ID = T14.ITEM_ID AND T90.STORE_CODE= T14.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151207' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T7
ON T90.ITEM_ID = T7.ITEM_ID AND T90.STORE_CODE = T7.STORE_CODE
LEFT JOIN 
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151209' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T5
ON T90.ITEM_ID = T5.ITEM_ID AND T90.STORE_CODE = T5.STORE_CODE
LEFT JOIN
(
  SELECT ITEM_ID,STORE_CODE,COUNT(*) AS RECORDS,SUM(qty_alipay_njhs) AS SALES FROM TC_CN_VALIDAT_20150929_1227_ST 
    WHERE TIME>='20151210' AND TIME <='20151213' GROUP BY ITEM_ID,STORE_CODE
)T3
ON T90.ITEM_ID = T3.ITEM_ID AND T90.STORE_CODE = T3.STORE_CODE;


-- 用平均值填补null
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET SALES60 = ROUND(SALES90*60/60,2) WHERE SALES60 IS NULL;
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET SALES30 = ROUND((SALES90*30/60+SALES60*30/60)/2,2) WHERE SALES30 IS NULL;
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET SALES14 = ROUND((SALES90*14/60+SALES60*14/60+SALES30*14/30)/3,2) WHERE SALES14 IS NULL;
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET SALES7 = ROUND((SALES90*7/60+SALES60*7/60+SALES30*7/30+SALES14*7/14)/4,2) WHERE SALES7 IS NULL;
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET SALES5 = ROUND((SALES90*5/60+SALES60*5/60+SALES30*5/30+SALES14*5/14+SALES7*5/7)/5,2) WHERE SALES5 IS NULL;
UPDATE TC_SALES_FEATURE_VALIDAT_ST SET 
  SALES3 = ROUND((SALES90*3/60+SALES60*3/60+SALES30*3/30+SALES14*3/14+SALES7*3/7+SALES5*3/5)/6,2) WHERE SALES3 IS NULL;




