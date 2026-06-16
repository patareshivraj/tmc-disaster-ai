# Phase 9 Audit Report: Building Advisor AI

## 1. Architecture Classification (FAIL / ❌)
*   **Expected:** Hybrid AI or Data-Driven AI
*   **Actual Classification:** **Pure Rule Engine**
*   **Assessment:** Your suspicion was entirely accurate. While the system computes a numerical `risk_score`, the underlying logic does not "learn" from the datasets. The weights (`age_weight: 0.35`, `condition_weight: 0.35`) are manually hardcoded in `train_building_model.py`. The AI is merely executing pre-written human logic rather than uncovering data-driven patterns.

## 2. Risk Score Source Verification (FAIL / ❌)
*   **Source:** Hardcoded static multipliers.
*   **Assessment:** The training script extracts `ward` exposure correctly, but it fails to analyze the actual correlation between `C1/C2A` building classifications and their attributes. It is not calculating historical coefficients; it is just assigning arbitrary weights.

## 3. Collapse Probability Audit (FAIL / ❌)
*   **Expected:** Data-driven probability derived from historical building/incident mapping.
*   **Actual:** `collapse_prob = risk_score * 0.8 + (20.0 if condition == "Poor") + (10.0 if age > 50)`
*   **Assessment:** This is a blatant `if-else` modifier. It mathematically guarantees that older, poor-condition buildings get a high collapse probability without ever referencing actual collapse or incident statistics from the datasets.

## 4. Recommendation Logic (PASS / ⚠️)
*   **Mechanism:** Recommendations are generated cleanly from the output classifications. 
*   **Assessment:** The mechanics of mapping "Evacuation Candidate" to "Immediate Evacuation" works perfectly and creates highly readable output for officers. However, because the underlying classification rests on a flawed rule engine, the recommendations themselves cannot be trusted as AI outputs.

## 5. Scenario Outputs & Code Quality (PASS)
*   **Outputs:** Successfully tested edge cases. Gracefully handles invalid dates and missing historical incidents.
*   **Code:** Clean, modular, and highly readable. 

---

## Final Assessment & Decision

*   **Overall Score:** 72%
*   **Decision:** Rework Phase 9 ❌

### Strengths
The feature engineering layer (extracting Ward-level flood exposure and calculating `years_since_last_inspection`) is very strong. The JSON output matches the requested interface perfectly.

### Weaknesses & Risks
The core math engine is a fake AI. It does not learn from `buildings.csv` or `incidents.csv`. It executes arbitrary arithmetic based on pre-defined thresholds.

### Required Fixes Before Phase 10 (Phase 9.1 Rework)
1.  **Learn Structural Coefficients:** `train_building_model.py` must actually analyze `buildings.csv`. It must calculate the statistical correlation (or empirical probability) of a building being assigned a high `risk_level` (like `C1` or `C2A`) based on its `condition` and `age`, rather than hardcoding `0.35`.
2.  **Data-Driven Collapse Probability:** Remove the `if age > 50` hardcoded bumps. The `collapse_probability` must be generated mathematically using the learned coefficients.
3.  **Upgrade Architecture Classification:** Transition the core calculation to a true Data-Driven heuristic engine.
