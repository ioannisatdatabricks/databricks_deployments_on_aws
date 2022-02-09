# Databricks notebook source
# MAGIC %md
# MAGIC # Example creating databases and tables in glue

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set the following values to reflect your installation

# COMMAND ----------

# The metastore database
metastoreDatabase = 'ioannis_papadopoulos_databricks_com'
# The bucket with the data
dataBucket = "dbs-ioannis-s3-bidirectional-crr-solution-workspace-bucket"
# The folder where the output of the data manipulation is stored
outputFolder = 'dbs-output'
outputPath = "s3a://" + dataBucket + '/' + outputFolder
bronzeUsersTableDataPath = outputPath + '/users_bronze_table'
bronzeUsersTableManifestPath = bronzeUsersTableDataPath + '/_symlink_format_manifest'

# COMMAND ----------

spark.sql(f"""
  CREATE DATABASE IF NOT EXISTS {metastoreDatabase}
""")
spark.sql(f"""
  USE {metastoreDatabase}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read the existing raw data, create a delta table, and register it to the Glue catalog

# COMMAND ----------

from pyspark.sql.functions import col, to_timestamp, to_date

# Read the raw data files
usersBronzeDF = (
    spark.read.json('s3a://' + dataBucket + '/retail-demo-data/users_json')
    .withColumn('creation_date', to_date(to_timestamp(col("creation_date"), "MM-dd-yyyy HH:mm:ss")))
    .withColumn('last_activity_date', to_date(to_timestamp(col("creation_date"), "MM-dd-yyyy HH:mm:ss")))
)
# Write to delta
usersBronzeDF.write.format("delta").mode("append").save(bronzeUsersTableDataPath)

# COMMAND ----------

spark.sql(f"""
  GENERATE symlink_format_manifest FOR TABLE delta.`{bronzeUsersTableDataPath}`
""")

# COMMAND ----------

# Register a table
spark.sql(f"""
  create table users_bronze
  using delta
  location '{bronzeUsersTableDataPath}'
""")

# COMMAND ----------

# Register another table
bronzeTableSchemaStringForGlue = usersBronzeDF.schema.simpleString().replace(":", " ").replace(",", ", ")[len('struct<'):-1]
spark.sql(f"""
  CREATE TABLE users_bronze_glue (
      {bronzeTableSchemaStringForGlue}
  )
  ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
  STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.SymlinkTextInputFormat'
  OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
  LOCATION '{bronzeUsersTableManifestPath}'
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC show tables

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from users_bronze order by creation_date

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clean up the environment

# COMMAND ----------

# Drop the tables from the metastore
spark.sql("drop table if exists users_bronze_glue")
spark.sql("drop table if exists users_bronze")

# COMMAND ----------

dbutils.fs.rm(outputPath, recurse = True)
