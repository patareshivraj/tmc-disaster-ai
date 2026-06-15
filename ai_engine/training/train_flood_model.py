import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

from ai_engine.features.flood_features import create_flood_features

def train_and_save_model():
    print("Extracting features using Phase 5 pipeline...")
    df = create_flood_features()

    print("Head of Feature DataFrame:")
    print(df.head())

    # Target and Features
    X = df.drop(columns=['date', 'has_flood'])
    y = df['has_flood']

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Preprocessing
    categorical_cols = ['ward']
    numeric_cols = ['rainfall_mm', 'humidity', 'water_level_m', 'temperature',
                    '3_day_avg_rainfall', '7_day_avg_rainfall', 'previous_flood_count', 'is_monsoon']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )

    # Model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('smote', SMOTE(random_state=42)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', max_depth=10))
    ])

    # =====================================================
    # K-FOLD CROSS VALIDATION (Phase 15.1 Hardening)
    # =====================================================
    print("Running 5-Fold Stratified Cross Validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        model, X, y, cv=cv,
        scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
        return_train_score=False
    )

    cv_metrics = {
        "accuracy": {"mean": round(float(np.mean(cv_results['test_accuracy'])) * 100, 2),
                     "std": round(float(np.std(cv_results['test_accuracy'])) * 100, 2)},
        "precision": {"mean": round(float(np.mean(cv_results['test_precision'])) * 100, 2),
                      "std": round(float(np.std(cv_results['test_precision'])) * 100, 2)},
        "recall": {"mean": round(float(np.mean(cv_results['test_recall'])) * 100, 2),
                   "std": round(float(np.std(cv_results['test_recall'])) * 100, 2)},
        "f1_score": {"mean": round(float(np.mean(cv_results['test_f1'])) * 100, 2),
                     "std": round(float(np.std(cv_results['test_f1'])) * 100, 2)},
        "roc_auc": {"mean": round(float(np.mean(cv_results['test_roc_auc'])) * 100, 2),
                    "std": round(float(np.std(cv_results['test_roc_auc'])) * 100, 2)},
    }
    print(f"Cross Validation Results: {json.dumps(cv_metrics, indent=2)}")

    # =====================================================
    # HOLDOUT EVALUATION
    # =====================================================
    print("Training Random Forest model with SMOTE...")
    model.fit(X_train, y_train)

    print("Evaluating model on holdout set...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    holdout_metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
        "recall": round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
        "roc_auc": round(roc_auc_score(y_test, y_proba) * 100, 2),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

    print(f"Holdout Metrics: {json.dumps(holdout_metrics, indent=2)}")

    # Save model and metrics
    os.makedirs('ai_engine/saved_models', exist_ok=True)
    joblib.dump(model, 'ai_engine/saved_models/flood_prediction.pkl')

    combined_metrics = {
        "version": "2.0 (Phase 15.1 Hardened)",
        "last_training_timestamp": datetime.now().isoformat(),
        "engine_type": "Random Forest Classifier with SMOTE",
        "cross_validation": cv_metrics,
        "holdout_evaluation": holdout_metrics,
        "validation_method": "5-Fold Stratified Cross Validation + 80/20 Holdout"
    }
    with open('ai_engine/saved_models/flood_model_metrics.json', 'w') as f:
        json.dump(combined_metrics, f, indent=4)

    print("Model and metrics saved successfully!")

if __name__ == "__main__":
    train_and_save_model()
