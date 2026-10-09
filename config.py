import os

# 1. Official Deutsche Börse Group GCP-Backed GraphQL Gateway Endpoint
# Reference: eurex.com/ex-en/data/free-reference-data-api
DBG_GRAPHQL_URL = "https://api.developer.deutsche-boerse.com/eurex-prod-graphql/"

# 2. Authentic Deutsche Börse Shared Rate-Limited Public Evaluation Key
# Passed via the mandatory institutional header parameter: X-DBP-APIKEY
DBG_GRAPHQL_KEY = os.getenv("DBG_GRAPHQL_KEY", "68cdafd2-c5c1-49be-8558-37244ab4f513")

# 3. Baseline Pipeline Tracking Variables
LOOKBACK_DAYS = 90
Z_SCORE_THRESHOLD = 3.0

os.makedirs("data", exist_ok=True)