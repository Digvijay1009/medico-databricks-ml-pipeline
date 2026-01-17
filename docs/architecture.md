## Architecture Overview

This project follows a Medallion Architecture pattern:

- **Bronze**: Raw healthcare data ingestion
- **Silver**: Data cleaning, validation, and schema enforcement
- **Gold**: Feature engineering for machine learning
- **ML**: Logistic Regression model training and evaluation
- **MLflow**: Experiment tracking, metrics, and model logging
- **Explainability**: Feature importance to interpret predictions

The architecture was validated first on small data and later scaled using synthetic healthcare records (~2000 rows).
