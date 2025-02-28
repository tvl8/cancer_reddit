import sparknlp
import pyspark
from sparknlp.annotator import *
from sparknlp.pretrained import *
from pyspark.sql import SparkSession

print("Spark NLP version: ", sparknlp.version())

## You need to add the spark-nlp jar to the spark session

spark = SparkSession.builder \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.5.1") \
    .getOrCreate()


print(f"Apache Spark version: {spark.version}")

spark.sparkContext.getConf().getAll()

import sys
print(f"Python version: {sys.version}")

from pip import _internal
print(f"pip version: {_internal.main(['show', 'pip'])}")

print("Pip packages:\n")
_internal.main(['list'])

print("Printing Spark COnfiguration")
print(spark.sparkContext.getConf().getAll())



print("Begin Spark NLP Test")


workspace_default_storage_account = "projectgstoragedfb938a3e"
workspace_default_container = "azureml-blobstore-becc8696-e562-432e-af12-8a5e3e1f9b0f"
workspace_wasbs_base_url = f"wasbs://{workspace_default_container}@{workspace_default_storage_account}.blob.core.windows.net/"


# Save the filtered subset to a Parquet file
input_path = f"{workspace_wasbs_base_url}not_cancer_subreddit.parquet"
data = spark.read.parquet(input_path)
data = data.select('body')
data = data.toDF('text')


print("Calling pretrained pipeline")

pipeline = PretrainedPipeline('analyze_sentiment', lang='en')

result = pipeline.transform(data)

result.show()

from sparknlp.functions import *

from sparknlp.annotation import Annotation

output_path = f"{workspace_wasbs_base_url}not_cancer_subreddit_sentiment.parquet"
result.write.parquet(output_path, mode='overwrite')


