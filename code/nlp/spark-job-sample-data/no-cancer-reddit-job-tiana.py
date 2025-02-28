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

print("Data Access Test")

blob_account_name = "dsan6000fall2024"
blob_container_name = "reddit-project"
wasbs_base_url = (
    f"wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/"
)
comments_path = "202306-202407/comments/"
submissions_path = "202306-202407/submissions/"

comments_df = spark.read.parquet(f"{wasbs_base_url}{comments_path}")
submissions_df = spark.read.parquet(f"{wasbs_base_url}{submissions_path}")

from pyspark.sql.functions import col, lower

# sample approximately 0.1 of the data
comments_subset_df = comments_df.sample(withReplacement=False, fraction=0.1, seed=42)

# Display the first few rows of subset DataFrame
comments_subset_df.show(5)

# Display the size (number of rows) in the df
print(f"Number of rows in the sampled and limited DataFrame: {comments_subset_df.count()}")

from pyspark.sql.functions import col, lower


# Filter for subreddits related to project
subreddit_list = ['CrohnsDisease', 'thyroidcancer', 'AskDocs', 'UlcerativeColitis', 'Autoimmune', 'BladderCancer', 'breastcancer', 'CancerFamilySupport', 'doihavebreastcancer', 'WomensHealth', 'ProstateCancer', 'cll', 'Microbiome', 'predental', 'endometrialcancer', 'cancer', 'Hashimotos', 'coloncancer', 'PreCervicalCancer', 'lymphoma', 'Lymphedema', 'CancerCaregivers', 'braincancer', 'lynchsyndrome', 'nursing', 'testicularcancer', 'leukemia', 'publichealth', 'Health', 'Fuckcancer', 'HealthInsurance', 'BRCA', 'Cancersurvivors', 'pancreaticcancer', 'skincancer', 'stomachcancer']

# Filter the DataFrame
filtered_comments_subset_df = comments_subset_df.filter(
    ~(col("subreddit").isin(subreddit_list))
)

# remove null subreddits
filtered_comments_subset_df = filtered_comments_subset_df.filter(col("body").isNotNull())

from pyspark.sql import functions as F
from pyspark.sql.functions import col, regexp_replace

# Sample DataFrame with text data in a 'text' column
filtered_comments_subset_df = filtered_comments_subset_df.withColumn('cleaned_body', col('body'))

# Remove leading and trailing whitespaces
filtered_comments_subset_df = filtered_comments_subset_df.withColumn('cleaned_body', F.trim(col('cleaned_body')))

# Remove punctuation (using regex)
filtered_comments_subset_df = filtered_comments_subset_df.withColumn('cleaned_body', regexp_replace(col('cleaned_body'), r'[^\w\s]', ''))

# Remove underscores
filtered_comments_subset_df = filtered_comments_subset_df.withColumn('cleaned_body', regexp_replace(col('cleaned_body'), '_', ''))

# Convert to lowercase
filtered_comments_subset_df = filtered_comments_subset_df.withColumn('cleaned_body', F.lower(col('cleaned_body')))
filtered_comments_subset_df = filtered_comments_subset_df.limit(10000)

# Preview the filtered DataFrame
filtered_comments_subset_df.show(5)

workspace_default_storage_account = "projectgstoragedfb938a3e"
workspace_default_container = "azureml-blobstore-becc8696-e562-432e-af12-8a5e3e1f9b0f"
workspace_wasbs_base_url = f"wasbs://{workspace_default_container}@{workspace_default_storage_account}.blob.core.windows.net/"


# Save the filtered subset to a Parquet file
output_path = f"{workspace_wasbs_base_url}not_cancer_subreddit.parquet"
filtered_comments_subset_df.write.parquet(output_path, mode="overwrite")

print(f"Test results saved to {output_path}")

print("Data Access Test Passed")


