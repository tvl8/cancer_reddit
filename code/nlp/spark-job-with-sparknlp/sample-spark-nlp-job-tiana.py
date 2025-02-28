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

#data = spark.createDataFrame([['Peter is a goud person.']]).toDF('text')

#data

workspace_default_storage_account = "projectgstoragedfb938a3e"
workspace_default_container = "azureml-blobstore-becc8696-e562-432e-af12-8a5e3e1f9b0f"
workspace_wasbs_base_url = f"wasbs://{workspace_default_container}@{workspace_default_storage_account}.blob.core.windows.net/"


# Save the filtered subset to a Parquet file
input_path = f"{workspace_wasbs_base_url}sample_submissions.parquet"
data = spark.read.parquet(input_path)
data = data.select('selftext')
data = data.toDF('text')


print("Calling pretrained pipeline")

pipeline = PretrainedPipeline('explain_document_ml')

result = pipeline.transform(data)

result.show()

from sparknlp.functions import *

from sparknlp.annotation import Annotation

def my_annoation_map_function(annotations):
    return list(map(lambda a: Annotation(
        'my_own_type',
        a.begin,
        a.end,
        a.result,
        {'my_key': 'custom_annotation_data'},
        []), annotations))

result.select(
    map_annotations(my_annoation_map_function, Annotation.arrayType())('token')
).toDF("my output").show(truncate=False)

explode_annotations_col(result, 'lemmas.result', 'exploded').select('exploded').show()

output_path = f"{workspace_wasbs_base_url}nlp_result_sample_submissions.parquet"
result.write.parquet(output_path, mode='overwrite')

