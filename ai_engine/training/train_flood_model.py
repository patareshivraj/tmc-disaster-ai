import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from ai_engine.features.flood_features import create_flood_features

def train_and_save_model():
    print("Extracting features using Phase 5 pipeline...")
    df = create_flood_features()
    
    # Verification as requested
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
    
    print("Training Random Forest model with SMOTE...")
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2),
        "recall": round(recall_score(y_test, y_pred) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred) * 100, 2),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"Metrics: {metrics}")
    
    # Save model and metrics
    os.makedirs('ai_engine/saved_models', exist_ok=True)
    joblib.dump(model, 'ai_engine/saved_models/flood_prediction.pkl')
    with open('ai_engine/saved_models/flood_model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print("Model and metrics saved successfully!")

if __name__ == "__main__":
    train_and_save_model()
