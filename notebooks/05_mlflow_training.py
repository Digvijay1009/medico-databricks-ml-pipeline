# Databricks notebook source
# DBTITLE 1,Cell 1
import mlflow
import mlflow.sklearn

mlflow.set_experiment("/Users/digvijayrengade8@gmail.com/healthcare_risk_prediction")

# COMMAND ----------

df = spark.table("medico_catalog.medico_db.gold_patient_features").toPandas()

X = df.drop("label", axis=1)
y = df["label"]


# COMMAND ----------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


# COMMAND ----------

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn

with mlflow.start_run(run_name="LogisticRegression_v1"):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("precision", precision_score(y_test, y_pred))
    mlflow.log_metric("recall", recall_score(y_test, y_pred))

    mlflow.sklearn.log_model(model, "model")
