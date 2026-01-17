# Databricks notebook source
import pandas as pd
import numpy as np
import random


# COMMAND ----------

NUM_RECORDS = 2000
np.random.seed(42)


# COMMAND ----------

data = []

for i in range(NUM_RECORDS):
    age = np.random.randint(18, 85)
    
    blood_pressure = np.random.randint(90, 180)
    glucose_level = np.random.randint(70, 260)
    cholesterol = np.random.randint(150, 320)
    bmi = round(np.random.uniform(18, 38), 1)
    
    smoking = np.random.choice(["yes", "no"], p=[0.35, 0.65])
    alcohol = np.random.choice(["yes", "no"], p=[0.30, 0.70])
    
    symptoms_count = np.random.randint(0, 7)
    
    # ---- Diagnosis Logic (IMPORTANT) ----
    risk_score = 0
    if glucose_level > 160: risk_score += 2
    if blood_pressure > 140: risk_score += 2
    if bmi > 30: risk_score += 1
    if smoking == "yes": risk_score += 1
    if symptoms_count >= 3: risk_score += 1
    
    diagnosis = 1 if risk_score >= 4 else 0
    
    # Add noise (realism)
    if random.random() < 0.08:
        diagnosis = 1 - diagnosis

    data.append([
        f"SYN_{i}", age, random.choice(["M", "F"]),
        blood_pressure, glucose_level, cholesterol,
        bmi, smoking, alcohol, symptoms_count, diagnosis
    ])


# COMMAND ----------

columns = [
    "patient_id", "age", "gender",
    "blood_pressure", "glucose_level",
    "cholesterol", "bmi",
    "smoking", "alcohol",
    "symptoms_count", "diagnosis"
]

pdf = pd.DataFrame(data, columns=columns)


# COMMAND ----------

sdf = spark.createDataFrame(pdf)


# COMMAND ----------

spark.table("medico_catalog.medico_db.patients").printSchema()


# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DecimalType

sdf_fixed = (
    sdf
    .withColumn("age", col("age").cast(IntegerType()))
    .withColumn("blood_pressure", col("blood_pressure").cast(IntegerType()))
    .withColumn("glucose_level", col("glucose_level").cast(IntegerType()))
    .withColumn("cholesterol", col("cholesterol").cast(IntegerType()))
    .withColumn("bmi", col("bmi").cast(DecimalType(4,1)))
    .withColumn("symptoms_count", col("symptoms_count").cast(IntegerType()))
    .withColumn("diagnosis", col("diagnosis").cast(IntegerType()))
)


# COMMAND ----------

sdf_fixed.write.format("delta") \
  .mode("append") \
  .saveAsTable("medico_catalog.medico_db.patients")


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM medico_catalog.medico_db.patients;
# MAGIC