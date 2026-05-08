from app.fetcher import get_token_overview, get_token_ohlcv
from app.scorer import score_token
from app.lifecycle import classify_lifecycle

# Use a small, simple test — 1 token, minimal calls
ADDRESS = "pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn"

print("Testing overview...")
overview = get_token_overview(ADDRESS)
print(f"Got overview keys: {list(overview.keys())[:5]}")

print("Testing OHLCV...")
ohlcv = get_token_ohlcv(ADDRESS)
print(f"Got ohlcv type: {type(ohlcv)}")

score_result = score_token(overview)
lifecycle_result = classify_lifecycle(overview, ohlcv)

print(f"\nRisk: {score_result['risk_label']} ({score_result['score']}/100)")
print(f"Verdict: {score_result['verdict']}")
print(f"Stage: {lifecycle_result['stage']}")
print(f"Explanation: {lifecycle_result['explanation'][:100]}")