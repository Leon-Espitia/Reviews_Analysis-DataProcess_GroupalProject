#!/usr/bin/python
import pandas as pd
import findspark
findspark.init()
from pyspark.sql import SparkSession

import pandas as pd

spark = (
  SparkSession
  .builder
  .master('yarn')
  .appName('bigquery-analytics-varsstdp')
  .getOrCreate()
)

bucket = 'spark-bucket-987'

spark.conf.set('temporaryGcsBucket', bucket)

df = spark.read.json('gs://testingnuevo/review.json')

df2 = pd.read_csv('gs://testingnuevo/Limpios/business.csv')

df2 = df2.select('business_id')

df2 = df2.withColumnRenamed("business_id","business_iddf2")

df3 = df2.join(df,df.business_id ==  df2.business_iddf2,"left")

df3.count()

df3 = df3.drop('business_iddf2')

# Spark saving

(
  df3.format('bigquery')
  .option('table', 'proyecto-grupal-369315.Henry.user')
  .mode('append')
  .save()
)
