import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import sha2, col
from google.cloud import secretmanager

spark = SparkSession.builder.appName("AlloyDB_to_BigQuery_ETL").getOrCreate()

# 1. Fetch the IP from environment variables
alloydb_ip = spark.conf.get("spark.alloydb.ip") 
project_id = spark.conf.get("spark.project.id")

# 2. Fetch the password securely from Secret Manager
client = secretmanager.SecretManagerServiceClient()
secret_name = f"projects/{project_id}/secrets/alloydb_mau_password/versions/latest"
response = client.access_secret_version(request={"name": secret_name})
db_password = response.payload.data.decode("UTF-8")

# 3. Connect to AlloyDB
alloydb_url = f"jdbc:postgresql://{alloydb_ip}:5432/telco_poc"
df = spark.read.format("jdbc") \
    .option("url", alloydb_url) \
    .option("dbtable", "synthetic_telco_churn") \
    .option("user", "mau") \
    .option("password", db_password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

# 4. Transform: De-identify sensitive data by hashing the CustomerID
df_transformed = df.withColumn("hashed_customerID", sha2(col("customerID"), 256)) \
                   .drop("customerID")

# 5. Load into BigQuery (Make sure to create 'my_dataset' in BQ first!)
df_transformed.write.format("bigquery") \
    .option("table", "my_dataset.telco_churn_analytics") \
    .option("temporaryGcsBucket", "hemauricio-data-foundation-poc") \
    .mode("overwrite") \
    .save()
