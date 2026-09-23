
import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# LOAD DATA
# ============================================================

DATA_DIR = Path("data/processed")

orders = pd.read_csv(DATA_DIR / "orders.csv")
deliveries = pd.read_csv(DATA_DIR / "deliveries.csv")
quality = pd.read_csv(DATA_DIR / "quality.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")


# ============================================================
# BASIC DATA VALIDATION
# ============================================================

print("=" * 60)
print("DATA VALIDATION")
print("=" * 60)

print("\nOrders:")
print(orders.shape)

print("\nDeliveries:")
print(deliveries.shape)

print("\nQuality:")
print(quality.shape)

print("\nSuppliers:")
print(suppliers.shape)


# Each order should have one delivery record
print("\nDelivery order_id unique:")
print(deliveries["order_id"].is_unique)

print("\nDuplicate delivery order IDs:")
print(
    deliveries["order_id"].duplicated().sum()
)


# ============================================================
# CONVERT DATES
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

deliveries["promised_date"] = pd.to_datetime(
    deliveries["promised_date"]
)

deliveries["actual_delivery_date"] = pd.to_datetime(
    deliveries["actual_delivery_date"]
)


# ============================================================
# CREATE DELIVERY OUTCOME
# ============================================================

deliveries["delivery_delay_days"] = (
    deliveries["actual_delivery_date"]
    - deliveries["promised_date"]
).dt.days

deliveries["is_late"] = (
    deliveries["actual_delivery_date"]
    > deliveries["promised_date"]
).astype(int)


# ============================================================
# CREATE ORDER-LEVEL QUALITY METRICS
# ============================================================

quality_summary = (
    quality
    .groupby("order_id")
    .agg(
        quantity_inspected=("quantity_inspected", "sum"),
        quantity_accepted=("quantity_accepted", "sum"),
        defective_quantity=("defective_quantity", "sum")
    )
    .reset_index()
)


# Safe division
quality_summary["quality_acceptance_rate"] = np.where(
    quality_summary["quantity_inspected"] > 0,
    quality_summary["quantity_accepted"]
    / quality_summary["quantity_inspected"],
    np.nan
)

quality_summary["defect_rate"] = np.where(
    quality_summary["quantity_inspected"] > 0,
    quality_summary["defective_quantity"]
    / quality_summary["quantity_inspected"],
    np.nan
)


# ============================================================
# MERGE ORDER + DELIVERY + QUALITY
# ============================================================

df = orders.merge(
    deliveries[
        [
            "order_id",
            "delivery_delay_days",
            "is_late"
        ]
    ],
    on="order_id",
    how="left",
    validate="one_to_one"
)

df = df.merge(
    quality_summary[
        [
            "order_id",
            "quality_acceptance_rate",
            "defect_rate"
        ]
    ],
    on="order_id",
    how="left",
    validate="one_to_one"
)

df = df.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "category",
            "location",
            "years_in_business"
        ]
    ],
    on="supplier_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# SORT CHRONOLOGICALLY
# ============================================================

df = df.sort_values(
    [
        "supplier_id",
        "order_date"
    ]
).reset_index(drop=True)


print("\n" + "=" * 60)
print("ORDER-LEVEL DATASET")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nLate delivery distribution:")
print(df["is_late"].value_counts())

print("\nSample:")
print(df.head())


# ============================================================
# HISTORICAL SUPPLIER FEATURES
# ============================================================
#
# IMPORTANT:
# These features use ONLY previous orders.
#
# Example:
#
# Order 5
#     ↓
# Use Orders 1-4
#     ↓
# Predict whether Order 5 is late
#
# We deliberately exclude the current order's delivery outcome
# from the historical features.
# ============================================================


# ------------------------------------------------------------
# 1. Number of previous orders
# ------------------------------------------------------------

df["prior_order_count"] = (
    df.groupby("supplier_id")
    .cumcount()
)


# ------------------------------------------------------------
# 2. Previous total spend
# ------------------------------------------------------------

df["prior_total_spend"] = (
    df.groupby("supplier_id")["total_amount"]
    .cumsum()
    - df["total_amount"]
)


# ------------------------------------------------------------
# 3. Previous average order value
# ------------------------------------------------------------

df["prior_avg_order_value"] = np.where(
    df["prior_order_count"] > 0,
    df["prior_total_spend"]
    / df["prior_order_count"],
    np.nan
)


# ------------------------------------------------------------
# 4. Previous number of late orders
# ------------------------------------------------------------

df["prior_late_count"] = (
    df.groupby("supplier_id")["is_late"]
    .cumsum()
    - df["is_late"]
)


# ------------------------------------------------------------
# 5. Previous late delivery rate
# ------------------------------------------------------------

df["prior_late_rate"] = np.where(
    df["prior_order_count"] > 0,
    df["prior_late_count"]
    / df["prior_order_count"],
    np.nan
)


# ------------------------------------------------------------
# 6. Previous total delivery delay
# ------------------------------------------------------------

df["prior_total_delay"] = (
    df.groupby("supplier_id")["delivery_delay_days"]
    .cumsum()
    - df["delivery_delay_days"]
)


# ------------------------------------------------------------
# 7. Previous average delivery delay
# ------------------------------------------------------------

df["prior_avg_delivery_delay"] = np.where(
    df["prior_order_count"] > 0,
    df["prior_total_delay"]
    / df["prior_order_count"],
    np.nan
)


# ------------------------------------------------------------
# 8. Previous quality acceptance rate
# ------------------------------------------------------------

quality_acceptance = (
    df["quality_acceptance_rate"]
    .fillna(0)
)

df["prior_quality_total"] = (
    quality_acceptance
    .groupby(df["supplier_id"])
    .cumsum()
    - quality_acceptance
)

df["prior_quality_acceptance_rate"] = np.where(
    df["prior_order_count"] > 0,
    df["prior_quality_total"]
    / df["prior_order_count"],
    np.nan
)


# ------------------------------------------------------------
# 9. Previous defect rate
# ------------------------------------------------------------

defect_rate = (
    df["defect_rate"]
    .fillna(0)
)

df["prior_defect_total"] = (
    defect_rate
    .groupby(df["supplier_id"])
    .cumsum()
    - defect_rate
)

df["prior_defect_rate"] = np.where(
    df["prior_order_count"] > 0,
    df["prior_defect_total"]
    / df["prior_order_count"],
    np.nan
)


# ============================================================
# CHECK HISTORICAL FEATURES
# ============================================================

historical_features = [
    "prior_order_count",
    "prior_total_spend",
    "prior_avg_order_value",
    "prior_late_rate",
    "prior_avg_delivery_delay",
    "prior_quality_acceptance_rate",
    "prior_defect_rate"
]

print("\n" + "=" * 60)
print("HISTORICAL FEATURES")
print("=" * 60)

print(
    df[
        [
            "supplier_id",
            "order_id",
            "order_date",
            "total_amount",
            "is_late"
        ] + historical_features
    ].head(15)
)


# ============================================================
# REMOVE FIRST SUPPLIER ORDERS
# ============================================================
#
# First order has no historical supplier information.
# Therefore we cannot calculate meaningful historical features
# for it.
# ============================================================

df = df[
    df["prior_order_count"] > 0
].copy()

print("\n" + "=" * 60)
print("AFTER REMOVING FIRST SUPPLIER ORDERS")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# DEFINE FEATURES AND TARGET
# ============================================================

feature_columns = [
    "total_amount",
    "years_in_business",
    "prior_order_count",
    "prior_total_spend",
    "prior_avg_order_value",
    "prior_late_rate",
    "prior_avg_delivery_delay",
    "prior_quality_acceptance_rate",
    "prior_defect_rate",
    "category",
    "location"
]

target_column = "is_late"


X = df[feature_columns]

y = df[target_column]


print("\n" + "=" * 60)
print("MODEL DATA")
print("=" * 60)

print("\nFeature columns:")
print(feature_columns)

print("\nX shape:")
print(X.shape)

print("\ny shape:")
print(y.shape)

print("\nTarget distribution:")
print(y.value_counts())

print("\nTarget percentage:")
print(y.value_counts(normalize=True))


# ============================================================
# TIME-BASED TRAIN / TEST SPLIT
# ============================================================
#
# We train on older orders and test on newer orders.
#
# This simulates the real business scenario:
#
# PAST DATA
#     ↓
# TRAIN
#     ↓
# FUTURE ORDERS
#     ↓
# TEST
# ============================================================

df = df.sort_values(
    "order_date"
).reset_index(drop=True)


split_index = int(
    len(df) * 0.80
)


train_df = df.iloc[
    :split_index
].copy()

test_df = df.iloc[
    split_index:
].copy()


X_train = train_df[
    feature_columns
]

y_train = train_df[
    target_column
]

X_test = test_df[
    feature_columns
]

y_test = test_df[
    target_column
]


print("\n" + "=" * 60)
print("TIME-BASED TRAIN / TEST SPLIT")
print("=" * 60)

print("\nTraining period:")
print(
    train_df["order_date"].min(),
    "to",
    train_df["order_date"].max()
)

print("\nTesting period:")
print(
    test_df["order_date"].min(),
    "to",
    test_df["order_date"].max()
)

print("\nTrain shape:")
print(X_train.shape)

print("\nTest shape:")
print(X_test.shape)


# ============================================================
# MACHINE LEARNING IMPORTS
# ============================================================

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# IDENTIFY FEATURE TYPES
# ============================================================

numeric_features = [
    "total_amount",
    "years_in_business",
    "prior_order_count",
    "prior_total_spend",
    "prior_avg_order_value",
    "prior_late_rate",
    "prior_avg_delivery_delay",
    "prior_quality_acceptance_rate",
    "prior_defect_rate"
]

categorical_features = [
    "category",
    "location"
]


# ============================================================
# NUMERICAL PREPROCESSING
# ============================================================

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        )
    ]
)


# ============================================================
# CATEGORICAL PREPROCESSING
# ============================================================

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# ============================================================
# COMBINE PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ============================================================
# RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print("TRAINING DELIVERY RISK MODEL")
print("=" * 60)

pipeline.fit(
    X_train,
    y_train
)

print("\nTraining completed.")


# ============================================================
# PREDICTIONS
# ============================================================

y_pred = pipeline.predict(
    X_test
)

y_probability = pipeline.predict_proba(
    X_test
)[:, 1]


print("\nPredictions generated.")

print("\nFirst 10 predictions:")
print(
    y_pred[:10]
)

print("\nFirst 10 risk probabilities:")
print(
    y_probability[:10]
)


# ============================================================
# MODEL EVALUATION
# ============================================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(
    f"\nAccuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)

print(
    f"ROC-AUC  : {roc_auc:.4f}"
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

feature_names = (
    pipeline
    .named_steps[
        "preprocessor"
    ]
    .get_feature_names_out()
)


importances = (
    pipeline
    .named_steps[
        "model"
    ]
    .feature_importances_
)


feature_importance = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": importances
    }
)


feature_importance = (
    feature_importance
    .sort_values(
        "importance",
        ascending=False
    )
    .reset_index(drop=True)
)


print("\n" + "=" * 60)
print("TOP FEATURE IMPORTANCE")
print("=" * 60)

print(
    feature_importance.head(15)
)


# ============================================================
# SAVE MODEL AND OUTPUTS
# ============================================================

import joblib


MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")


MODEL_DIR.mkdir(
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)


# ------------------------------------------------------------
# Save model
# ------------------------------------------------------------

joblib.dump(
    pipeline,
    MODEL_DIR / "delivery_risk_model.pkl"
)


# ------------------------------------------------------------
# Save predictions
# ------------------------------------------------------------

predictions = test_df[
    [
        "order_id",
        "supplier_id",
        "supplier_name",
        "order_date",
        "total_amount",
        "is_late"
    ]
].copy()


predictions[
    "predicted_is_late"
] = y_pred


predictions[
    "late_probability"
] = y_probability


predictions.to_csv(
    OUTPUT_DIR / "delivery_risk_predictions.csv",
    index=False
)


# ------------------------------------------------------------
# Save feature importance
# ------------------------------------------------------------

feature_importance.to_csv(
    OUTPUT_DIR / "delivery_risk_feature_importance.csv",
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("FILES SAVED")
print("=" * 60)

print(
    "\nModel:"
)

print(
    "models/delivery_risk_model.pkl"
)

print(
    "\nPredictions:"
)

print(
    "outputs/delivery_risk_predictions.csv"
)

print(
    "\nFeature importance:"
)

print(
    "outputs/delivery_risk_feature_importance.csv"
)

print("\n" + "=" * 60)
print("DELIVERY RISK ML PIPELINE COMPLETE")
print("=" * 60)

