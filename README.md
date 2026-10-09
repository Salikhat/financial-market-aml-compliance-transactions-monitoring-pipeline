# Financial Fraud, AML/CFT & Transaction Monitoring Tuning Pipeline

## 📝 Project Overview & Core Capabilities
This repository houses a quantitative data engineering and statistical validation engine built to model institutional transaction risk, eliminate compliance alert fatigue, and automate risk detection protocols within high-volume financial exchange infrastructures.

### 🔍 Key Capabilities Deployed (Updated Build):
*   **Enterprise GraphQL Ingestion Engine:** Replaced the legacy `yfinance` endpoint with an authenticated, token-gated HTTPS POST connection structure targeting the **Deutsche Börse Group API Platform** and **Eurex/Clearstream Developer Gateways**.
*   **ISO 20022 Payloads Parsing:** Automates the handling of custom API keys (`X-DBP-APIKEY`), executes complex graph queries (`SettlementInstructions` schema), and flattens deeply nested JSON objects into normalized data matrix formats.
*   **Advanced Feature Engineering:** Replicates complex SQL window functions using Python to generate rolling 90-day behavioral baselines (μ, σ) per market participant, completely eliminating lookahead bias.
*   **BaFin-Compliant Scenario Tuning:** Employs a non-parametric **Two-Sample Kolmogorov-Smirnov (KS) Test** to perform empirical **Below-the-Line (BTL)** validation checks, mathematically proving to regulatory auditors that unalerted transaction tranches carry zero compliance leakage risk.
*   **Classification Optimization:** Builds custom **ROC / AUC curves** and solves for the maximum **Youden’s J Statistic** to pinpoint the exact alert threshold that suppresses false-positive noise while keeping true risk capture locked at 100%.

### 🏛️ Regulatory & Industry Alignment:
This portfolio asset is explicitly designed to meet model validation transparency expectations dictated under **Section 6 of the German Money Laundering Act (Geldwäschegesetz - GwG)**, federal supervisory mandates (**BaFin**), and the unified **EU Anti-Money Laundering Regulation (AMLR)** single-rulebook frameworks.

---

## 📅 Daily Operational Mapping (Senior Data Analyst Duties)
This codebase is systematically segmented to replicate the daily workflow of an institutional Compliance Data Analyst:
1. **Automated Ingestion Monitoring (`src/data_ingestion.py`):** Replicates checking morning data feeds and API pipeline health to stage raw trading/clearing volumes into core ledger systems.
2. **High-Dimensional Deep Dives (`src/data_cleaning.py`):** Simulates cleaning transactional data logs and constructing dynamic behavioral peer-group rolling profiles.
3. **Scenario Tuning & Risk Validation (`src/statistical_modeling.py`):** Executes Above-the-Line (ATL) and Below-the-Line (BTL) testing cycles to scientifically calibrate risk engines, eliminating alert fatigue while preventing regulatory leaks.
4. **Audit Reporting (`data/final_compliance_output.csv`):** Compiles immutable analytical logs for the **Money Laundering Reporting Officer (MLRO)** and external regulatory reviews.

---

## 🛠️ Installation & Execution Protocol

To establish your sandboxed environment and execute the compliance cycle, run the following sequence in your terminal:

```bash
# Initialize local virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required mathematical and data engineering packages
./venv/bin/pip install pandas numpy scipy scikit-learn yfinance

# Execute Stage 1: Live Market API Ingestion Simulation
./venv/bin/python3 src/data_ingestion.py

# Execute Stage 2: Database Layer Cleansing & Moving Feature Engineering
./venv/bin/python3 src/data_cleaning.py

# Execute Stage 3: Quantitative Scenario Validation & Tuning Optimization
./venv/bin/python3 src/statistical_modeling.py
```

*For an exhaustive breakdown of the mathematical equations, statistical theories, and structural design choices used across this platform, refer to the accompanying [ARCHITECTURE_AND_METHODOLOGY.md](./ARCHITECTURE_AND_METHODOLOGY.md) technical whitepaper.*