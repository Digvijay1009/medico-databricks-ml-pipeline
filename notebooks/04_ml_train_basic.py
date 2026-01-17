# Databricks notebook source
df = spark.table("medico_catalog.medico_db.gold_patient_features").toPandas()

X = df.drop("label", axis=1)
y = df["label"]

print(X.shape, y.shape)


# COMMAND ----------

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X, y)

print("✅ Model trained successfully")


# COMMAND ----------

pred = model.predict(X)
print("Predictions:", pred)


# COMMAND ----------

# DBTITLE 1,Train–Test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


# COMMAND ----------

model = LogisticRegression()


# COMMAND ----------

# DBTITLE 1,Re-train Model
model = LogisticRegression(max_iter=1000)

model.fit(X_train,y_train)

print("Model trianed successfully")

# COMMAND ----------

# DBTITLE 1,Evaluate Model
from sklearn.metrics import accuracy_score, precision_score, recall_score

y_pred = model.predict(X_test)

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
