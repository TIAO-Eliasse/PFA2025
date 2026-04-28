# SME Survival Analytics (Engineering Thesis Research)

Advanced machine learning framework for predicting SME (Small and Medium Enterprise) survival, originally developed as an engineering thesis at **ISSEA-CEMAC, Cameroon**.

## 🎯 Research Objective
To provide financial institutions with a robust, interpretable credit-scoring tool by modeling the probability of survival for local enterprises over time.

## 🛠 Methodology
- **Predictive Engine:** Benchmark of Gradient Boosting (XGBoost, CatBoost) vs. Random Survival Forests.
- **Performance:** Achieved a **C-index of 0.70**.
- **Explainability:** Integrated **SHAP-based attribution** to decompose risk factors for each specific decision, ensuring transparency for policy analysts.

## 🏗 Components
- Accueil.py: Streamlit frontend for the risk monitoring dashboard.
- Models/: Serialized ML models for survival prediction.
- data/: Preprocessing pipelines for fiscal and census data integration.
