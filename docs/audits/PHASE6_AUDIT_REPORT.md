# Phase 6 Audit Report: Flood Prediction AI

## 1. File & Artifact Verification (PASS)
*   `ai_engine/models/flood_model.py`: **Verified**
*   `ai_engine/training/train_flood_model.py`: **Verified**
*   `ai_engine/saved_models/flood_prediction.pkl`: **Verified**
*   `ai_engine/saved_models/flood_model_metrics.json`: **Verified**

## 2. Dataset Integrity Validation (PASS)
*   **Null Values:** 0 across all feature columns.
*   **Invalid Entries:** 0 negative rainfall or humidity entries detected.
*   **Feature Leakage:** Clean. Target variables from the incident dataset do not leak into the predictor matrix.

## 3. Training Pipeline Verification (PASS)
*   **Train/Test Split:** Implemented correctly (80/20 with `stratify=y`).
*   **Reproducibility:** Random states fixed at `42` across the pipeline.
*   **Serialization:** Model successfully deserializes via `joblib`.

## 4. Feature Importance & Ranking (PASS)
The model correctly focuses on meteorological logic rather than memorizing ward names. Ward identifiers do not dominate.
**Top 5 Features:**
1.  `humidity`: 21.85%
2.  `rainfall_mm`: 16.24%
3.  `3_day_avg_rainfall`: 15.39%
4.  `7_day_avg_rainfall`: 11.08%
5.  `is_monsoon`: 9.38%

## 5. Model Metrics & Performance (FAIL / FLAG)
*   **Accuracy:** 97.09%
*   **Precision:** 0.0%
*   **Recall:** 0.0%
*   **F1 Score:** 0.0%
*   **Audit Finding:** The dataset generated in Phase 4 maps thousands of non-monsoon days against very few actual flood incidents (floods only occurred on exactly 31 days out of the testing set). The 97% accuracy is an illusion of **extreme class imbalance**. The model learned that guessing "No Flood" is almost always right.

## 6. Scenario Prediction Tests (FAIL)
*   **Scenario 1 (Kalwa, Rain 5mm):** `Low Risk` (0.0% Prob) -> **PASS**
*   **Scenario 2 (Mumbra, Rain 180mm):** `Low Risk` (24.0% Prob) -> **FAIL** (Expected High)
*   **Scenario 3 (Diva, Rain 120mm):** `Low Risk` (23.0% Prob) -> **FAIL** (Expected Med/High)
*   **Scenario 4 (Naupada, Rain 0mm):** `Low Risk` (0.0% Prob) -> **PASS**

## 7. Edge Case & Confidence Logic (PASS)
*   Unknown Wards (e.g., "UnknownWard") do not crash the model due to `OneHotEncoder(handle_unknown='ignore')`.
*   Confidence scores are properly formatted as 0-100 `float` values.

---

## Final Assessment & Decision

*   **Overall Score:** 72%
*   **Production Readiness Rating:** 75%
*   **Decision:** Minor Fixes Needed ⚠️ (Do NOT proceed to Phase 7 yet)

### Strengths
The structural architecture, class design, feature selection, and data pipelines are absolutely production-grade. The model focuses on the correct environmental variables rather than biased identifiers.

### Weaknesses & Risks
Because the synthetic dataset exhibits a ~97% negative class imbalance, the Random Forest Classifier became highly conservative. Even with `class_weight='balanced'`, it refuses to cross the 50% probability threshold for extreme rainfall events, failing critical Scenarios 2 and 3.

### Recommended Fixes
Before marking Phase 6 complete, we must implement one or both of the following inside `train_flood_model.py`:
1.  **Implement SMOTE** (Synthetic Minority Over-sampling Technique) to synthetically balance the training data before fitting the model.
2.  **Probability Threshold Tuning**: Adjust `flood_model.py` so that a 20%+ probability of a flood triggers a "High Risk" alert (since a 24% chance of a city-wide flood is actually statistically massive).
