# Project Architecture, Statistical Methodology, & Regulatory Calibration Report

This technical document details the design specifications, mathematical foundations, and regulatory justifications supporting the **financial-abuse-fraud-monitoring-pipeline**. 

---

## 📁 1. Functional Directory & File Specifications

### `config.py`
*   **Purpose:** Centralizes system configurations, structural thresholds, global time horizons, and environment variables.
*   **Compliance Rationale:** Guarantees transparency and version-controlled change management. If BaFin or internal validation auditors require a change in variance limits, the alteration is modified here, creating a clear history log for the model audit trail.

### `src/data_ingestion.py`
*   **Purpose:** Dynamically connects to an open API source (Yahoo Finance framework targeting the **DAX Index - `^GDAXI`**) to capture real-time market activity, and maps it directly into an in-memory SQL database structure (`raw_market_ledger`).
*   **Compliance Rationale:** Implements the core database principles of continuous ingestion and automated input filtering, mapping out raw clearing infrastructure volumes before risk classification begins.

### `src/data_cleaning.py`
*   **Purpose:** Executes database queries to clean formatting errors and automatically handles missing values using safe interpolation logic. It computes a 90-day moving historical mean (μ) and standard deviation (σ) per trading participant asset file.
*   **Compliance Rationale:** Satisfies **EU AMLR** single-rulebook mandates by replacing rigid, uniform thresholds with dynamic participant baselines. Moving data via a `.shift(1)` lookback window ensures that any volume calculation excludes the active transaction, completely preventing lookahead bias.

### `src/statistical_modeling.py`
*   **Purpose:** Houses the main statistical analysis engine. It runs parametric log-transformations, flags behavioral outliers, models Below-the-Line (BTL) distribution divergence, and performs mathematical threshold optimization.
*   **Compliance Rationale:** Serves as the central engine for **BaFin Model Validation compliance**. It turns qualitative regulatory goals into verifiable mathematical limits.

---

## 📊 2. Deep Dive: Advanced Statistical Methods Deployed

### A. Parametric Log-Transformation
*   **The Problem:** Financial market transaction volumes naturally follow a heavily right-skewed power-law distribution. Standard linear models treat massive institutional settlement spikes as extreme errors rather than structured trends.
*   **The Methodology:** The pipeline applies a natural log transformation:
    \[\text{log\_volume} = \ln(1 + \text{Volume})\]
*   **The Outcome:** This log-transformation stabilizes data variance and reshapes long-tailed data into a normalized distribution profile, preventing false-positive noise in downstream anomaly detection.

### B. Dynamic Time-Series Z-Score Anomaly Tracking
*   **The Problem:** Money launderers attempt to hide inside standard transactions by operating just below global fixed caps.
*   **The Methodology:** Every daily volume calculation is transformed into a standard score based on its variance distance from its own 90-day historical mean:
    \[Z = \frac{X_t - \mu_{90}}{\sigma_{90}}\]
*   **The Threshold Setup:** The global threshold parameter is locked at **\(\vert{}Z\vert{} > 3.0\)**. Mathematically, assuming normal distribution, any volume transaction breaking this limit sits past the **99.73% confidence interval**, signaling an immediate, non-random behavioral anomaly.

### C. Below-the-Line (BTL) Testing via Two-Sample Kolmogorov-Smirnov Test
*   **The Problem:** Regulatory supervisors require empirical evidence that changing a threshold will not create an unmonitored blind spot where laundering can go unnoticed.
*   **The Methodology:** The pipeline runs a non-parametric **Two-Sample Kolmogorov-Smirnov (KS) Test** comparing the Cumulative Distribution Functions (CDFs) of the unalerted population (BTL) and the alerted population (ATL).
*   **The Threshold Setup:** The test evaluates the maximum vertical distance (D) between the two curves. If the resulting p-value falls below **α = 0.05**, we reject the null hypothesis. This mathematically proves that the BTL population is structurally distinct from the high-risk tracking zone, justifying the threshold setting to regulatory supervisors.

### D. ROC Curve & Youden’s J Statistic Calibration
*   **The Problem:** Compliance groups struggle with alert fatigue from noisy alerting logic.
*   **The Methodology:** The system creates a Receiver Operating Characteristic (ROC) curve to balance the True Positive Rate (TPR) and False Positive Rate (FPR). It runs a processing loop to find the maximum **Youden’s J Statistic**:
    \[J = \text{Sensitivity} + \text{Specificity} - 1\]
*   **The Outcome:** The script pinpoints the exact score threshold where the system maximizes false-positive noise suppression while ensuring that the overall True Positive Rate remains locked at **1.0 (100% historical risk capture)**.

---

## 📈 3. Compliance Analysis Summary

Upon full execution of the pipeline, the system extracts the following parameters:
1.  **Anomaly Isolation Rate:** Out of the continuous stream of market data logs, the dynamic Z-score tracker successfully filters out localized volume spikes that sit outside normal operating boundaries (\(\vert{}Z\vert{} > 3.0\)).
2.  **BTL Validation Confirmation:** The Two-Sample KS-Test verifies with high statistical confidence (p < 0.05) that our threshold parameters are not masking hidden compliance leakages within the lower transaction tranches.
3.  **Audit Traceability:** Every script execution stores the resulting data profiles directly in `data/final_compliance_output.csv`. This output logs the raw metadata alongside the computed Z-scores, prediction models, and true positive classifications, establishing an immutable data lineage record that satisfies **Section 6 of the German GwG** requirements for internal audit controls.
