# Databricks notebook source
import mlflow.sklearn

model_uri = "runs:/7a8e5c11b5b845d7b3dd19e464e6ab26/model"
model = mlflow.sklearn.load_model(model_uri)


# COMMAND ----------

df = spark.table("medico_catalog.medico_db.gold_patient_features").toPandas()
X = df.drop("label", axis=1)


# COMMAND ----------

import pandas as pd

importance = pd.Series(model.coef_[0], index=X.columns)
importance.sort_values().plot(kind="barh",figsize=(8,5), title="Feature Importance -  Healthcare Risk Model")


# COMMAND ----------

# DBTITLE 1,model signature + input example
import pandas as pd

# Load data again (safe habit)
df = spark.table("medico_catalog.medico_db.gold_patient_features").toPandas()
X = df.drop("label", axis=1)

# Take 1 row as example
input_example = X.head(1)


# COMMAND ----------

import numpy as np

# Reload data safely
df = spark.table("medico_catalog.medico_db.gold_patient_features").toPandas()

# Convert Decimal columns to float
X = df.drop("label", axis=1).astype(float)

y = df["label"]


# COMMAND ----------

input_example = X.head(1)


# COMMAND ----------

from mlflow.models.signature import infer_signature
import mlflow
import mlflow.sklearn

signature = infer_signature(X, model.predict(X))

with mlflow.start_run(run_name="LogisticRegression_with_signature_clean"):
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        signature=signature,
        input_example=input_example
    )
