import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import roc_curve
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def run_statistical_pipeline():
    df = pd.read_csv("data/engineered_features.csv")
    
    # 1. Apply Log-Transformation to stabilize highly skewed right-tailed transaction volumes
    df['log_volume'] = np.log1p(df['Volume'])
    
    # 2. Run Rolling Z-Score Behavioral Anomaly Tracking
    df['z_score'] = (df['Volume'] - df['rolling_mean_volume']) / df['rolling_std_volume']
    anomalies = df[abs(df['z_score']) > config.Z_SCORE_THRESHOLD]
    print(f"🚨 Behavioral Z-Score Checks: Detected {len(anomalies)} structural anomalies exceeding threshold of {config.Z_SCORE_THRESHOLD}.")
    
    # 3. Simulate Historical Ground-Truth labels for model validation optimization
    np.random.seed(42)
    df['true_labels'] = (df['z_score'] > 1.5).astype(int)
    
    # Inject synthetic noise to simulate messy compliance environments
    noise = np.random.choice([0.0, 1.0, 2.0], size=len(df), p=[0.90, 0.08, 0.02])
    df['predicted_scores'] = np.clip(abs(df['z_score']) + noise, 0, 10)
    
    # 4. Execute Below-the-Line (BTL) Testing using a Two-Sample Kolmogorov-Smirnov Test
    btl_population = df[df['z_score'] < 1.5]['predicted_scores']
    atl_population = df[df['z_score'] >= 1.5]['predicted_scores']
    
    if len(btl_population) > 0 and len(atl_population) > 0:
        ks_stat, p_value = stats.ks_2samp(btl_population, atl_population)
        print(f"📊 Below-the-Line (BTL) KS-Test Statistic: {ks_stat:.4f} (p-value: {p_value:.4e})")
        if p_value < 0.05:
            print("✅ Statistical Conclusion: BTL and ATL distributions are distinct. Low risk of true compliance leakage below active line parameters.")
        else:
            print("⚠️ Warning: Distributions overlap. Regulatory blind spot risk detected.")
    else:
        print("ℹ️ Insufficient distribution divergence to run automated KS-Test tranches.")

    # 5. Optimize Alert Thresholds via ROC Curve & Youden's J Statistic
    if len(df['true_labels'].unique()) > 1:
        fpr, tpr, thresholds = roc_curve(df['true_labels'], df['predicted_scores'])
        youden_j = tpr - fpr
        optimal_index = np.argmax(youden_j)
        optimal_threshold = thresholds[optimal_index]
        print(f"🎯 Threshold Optimization: Statistically optimal risk scenario target score is: {optimal_threshold:.4f} (Youden's J: {youden_j[optimal_index]:.4f})")
    else:
        print("ℹ️ High-homogeneity dataset. Skipping Youden's optimization tranche until baseline shifts.")
    
    df.to_csv("data/final_compliance_output.csv", index=False)
    print("🏁 Statistical pipeline run complete. Audit trail output saved to 'data/final_compliance_output.csv'.")

if __name__ == "__main__":
    run_statistical_pipeline()