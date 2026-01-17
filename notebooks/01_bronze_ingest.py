# Databricks notebook source
df = spark.read.option("header", True).csv("/Volumes/medico_catalog/medico_db/bronze_volume/patients.csv")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM medico_catalog.medico_db.patients;
# MAGIC