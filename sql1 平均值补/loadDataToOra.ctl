load data
infile 'C:\Users\Administrator\Desktop\ML\cainiao\data\item_feature1.csv'
into table TC_CAINIAO_ITEM_FEATURE
fields terminated by ','
( 
  time,
  ITEM_ID,
  CATE_ID,
  CATE_LEVEL_ID,
  BRAND_ID,
  SUPPLIER_ID,
  PV_IPV, 
  PV_UV,
  CART_IPV,
  CART_UV ,
  COLLECT_UV,
  NUM_GMV,
  AMT_GMV,
  QTY_GMV,
  UNUM_GMV,
  AMT_ALIPAY,
  NUM_APLIPAY,
  QTY_APIPAY,
  UNUM_ALIPAY,
  ZTC_PV_IPV,
  TBK_PV_IPV,
  SS_PV_IPV,
  JHS_PV_IPV,
  ZTC_PV_UV,
  TBK_PV_UV,
  SS_PV_UV,
  JHS_PV_UV,
  NUM_AIPAY_HJHS,
  AMT_APLIPAY_NJHS,
  QTY_ALIPAY_NJHS,
  UNUM_ALIPAY_NJHS
 )

