# Databricks notebook source
display(spark.table("medico_catalog.medico_db.patients_silver"))

# COMMAND ----------

from pyspark.sql.functions import when, col

df = spark.table("medico_catalog.medico_db.patients_silver")

df_gold = (
    df.withColumn("smoking", when(col("smoking")=="yes",1).otherwise(0))
      .withColumn("alcohol", when(col("alcohol")=="yes",1).otherwise(0))
      .withColumnRenamed("diagnosis", "label")
      .select(
          "age","blood_pressure","glucose_level","cholesterol",
          "bmi","symptoms_count","smoking","alcohol","label"
      )
)

df_gold.write.format("delta") \
  .mode("overwrite") \
  .saveAsTable("medico_catalog.medico_db.gold_patient_features")


# COMMAND ----------

display(spark.table("medico_catalog.medico_db.gold_patient_features"))