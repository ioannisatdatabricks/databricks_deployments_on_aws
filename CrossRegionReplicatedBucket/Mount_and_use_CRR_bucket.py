# Databricks notebook source
# MAGIC %md
# MAGIC # Example mounting and using an external S3 bucket, which is cross-region replicated

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set the following values (mount point, bucket names) to reflect your installation

# COMMAND ----------

# The mount point for the bucket to be accessed by Databricks
mountPoint = "/mnt/demo-data"
# The bucket in the same region where the Databricks workspace is deployed
workspaceBucket = "dbs-ioannis-s3-bidirectional-crr-solution-workspace-bucket"
# The bucket in the region where the data were originally generated
sourceBucket = "dbs-ioannis-s3-bidirectional-crr-solution-source-bucket"
# The metastore database
metastoreDatabase = 'ioannis_papadopoulos_databricks_com'

# COMMAND ----------

spark.sql(f"""
  create database if not exists {metastoreDatabase}
""")
spark.sql(f"""
  use {metastoreDatabase}
""")

# COMMAND ----------

# DBTITLE 1,Current mount points
# MAGIC %fs mounts

# COMMAND ----------

# DBTITLE 1,Unmount previously mount point, if exists
if next((mount for mount in dbutils.fs.mounts() if mount.mountPoint == mountPoint), None) is not None:
    dbutils.fs.unmount(mountPoint)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Mount the bucket in the same region and remove previous output if needed

# COMMAND ----------

dbutils.fs.mount('s3a://' + workspaceBucket, mountPoint)

# COMMAND ----------

# DBTITLE 1,Show the contents using the mount point
# MAGIC %fs ls /mnt/demo-data

# COMMAND ----------

# DBTITLE 1,Remove the previous output if it exists
outputFolder = 'dbs-output'
if next((folder for folder in dbutils.fs.ls(mountPoint) if folder.name == outputFolder+'/'), None):
    dbutils.fs.rm(mountPoint+'/'+outputFolder, recurse=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read the existing raw data, create a delta table, and manipulate the data

# COMMAND ----------

from pyspark.sql.functions import col, to_timestamp, to_date

# Read the raw data files
usersBronzeDF = (
    spark.read.json('/mnt/demo-data/retail-demo-data/users_json')
    .withColumn('creation_date', to_date(to_timestamp(col("creation_date"), "MM-dd-yyyy HH:mm:ss")))
    .withColumn('last_activity_date', to_date(to_timestamp(col("creation_date"), "MM-dd-yyyy HH:mm:ss")))
)

# Write to delta
bronzeUsersTableDataPath = mountPoint + '/' + outputFolder + '/users_bronze_table'
usersBronzeDF.write.format("delta").mode("append").save(bronzeUsersTableDataPath)

# Register a table
spark.sql(f"""
  create table users_bronze
  using delta
  location '{bronzeUsersTableDataPath}'
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from users_bronze order by creation_date

# COMMAND ----------

# Delete some entries and vacuum the files
spark.sql("""
    delete from users_bronze where creation_date < '2000-01-02'
""")
spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", False)
spark.sql("""
    VACUUM users_bronze RETAIN 0 HOURS
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Compare the data in the S3 buckets

# COMMAND ----------

import boto3
s3 = boto3.client('s3')

# COMMAND ----------

filesInWorkspaceBucket = set([f['Key'] for f in s3.list_objects(Bucket=workspaceBucket, Prefix=outputFolder)['Contents']])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Give it up to 15 minutes for the replication to complete and then compare the files

# COMMAND ----------

filesInSourceBucket = set([f['Key'] for f in s3.list_objects(Bucket=sourceBucket, Prefix=outputFolder)['Contents']])
assert(filesInWorkspaceBucket == filesInSourceBucket)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clean up the environment

# COMMAND ----------

spark.sql("""
    drop table if exists users_bronze
""")
dbutils.fs.rm(mountPoint+'/'+outputFolder, recurse=True)
