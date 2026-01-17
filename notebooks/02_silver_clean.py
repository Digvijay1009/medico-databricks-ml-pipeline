# Databricks notebook source
df = spark.table("medico_catalog.medico_db.patients")

# COMMAND ----------

from pyspark.sql.functions import col

df_silver = (
    df.withColumn("age", col("age").cast("int"))
      .filter(col("age").between(0, 100))
      .dropDuplicates(["patient_id"])
)

# COMMAND ----------

df_silver.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("medico_catalog.medico_db.patients_silver")

# COMMAND ----------

display(spark.table("medico_catalog.medico_db.patients_silver"))

# COMMAND ----------

# MAGIC %sql
# MAGIC Select * from medico_catalog.medico_db.patients_silver