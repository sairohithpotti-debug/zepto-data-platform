# Module 2: Analytics Pipeline (/analytics)

## Overview
This module executes a data-profiling, exploratory data analysis, data storytelling, and predictive-modeling pipeline on the Titanic dataset.

## Folder Structure

analytics/
├── titanic.csv               # Offline fallback dataset
├── 01_eda.ipynb              # EDA & Profiling Notebook
├── 02_modeling.ipynb         # Modeling & Pipeline Evaluation Notebook
├── best_titanic_pipeline.pkl # Saved joblib pipeline artifact
└── README.md                 # Documentation & Written Story


## 1. Missing Value Strategy & Outlier Analysis
- *Missing Value Rules:*
  - < 5% missing: Dropped rows (embarked, embark_town).
  - 5% - 30% missing: Median imputation for numerical fields (age), mode for categorical fields.
  - > 30% missing: Column dropped (deck).
- *Outliers (IQR Rule):*
  - Both age and fare exhibit extreme values. fare is highly right-skewed with a significant gap between median and mean.

## 2. Bivariate Analysis & Feature Correlations
- *Key Findings:*
  - Females have higher survival rates across all passenger classes compared to males.
  - 1st class passengers show higher survival rates than 2nd and 3rd class passengers.
- *Top Off-Diagonal Correlations:*
  - Strongest negative correlation: pclass and fare (higher classes paid significantly higher fares).
  - Second strongest correlation: pclass and survived.

## 3. Model Performance Summary

### Classifier Comparison Table
| Model | Accuracy | Precision | Recall | F1 Score | AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *Logistic Regression* | 0.804 | 0.771 | 0.710 | 0.739 | 0.852 |
| *Decision Tree* | 0.788 | 0.782 | 0.623 | 0.694 | 0.821 |
| *Random Forest (Tuned)* | *0.821* | *0.810* | *0.725* | *0.763* | *0.871* |

### Imbalance Handling Strategy
- class_weight='balanced' achieved the best trade-off between Precision and Recall.

### Regression Sub-Task (Predicting Fare)
- Multivariate linear regression on fare demonstrated heteroscedasticity, visible via the widening residual spread at higher predicted values.

## Deployment Recommendation
Deploy *best_titanic_pipeline.pkl* (Tuned Random Forest). It achieves the highest F1 score and AUC while fully encapsulating preprocessing within the scikit-learn pipeline, preventing data leakage during inference.
