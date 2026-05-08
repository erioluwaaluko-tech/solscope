from app.fetcher import get_token_overview, get_token_ohlcv

ADDRESS = "pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn"

print("Testing overview...")
overview = get_token_overview(ADDRESS)
print(f"All overview keys: {list(overview.keys())}")
print(f"marketCap value: {overview.get('marketCap')}")
print(f"mc value: {overview.get('mc')}")

print("\nTesting OHLCV...")
ohlcv = get_token_ohlcv(ADDRESS)
print(f"OHLCV keys: {list(ohlcv.keys()) if isinstance(ohlcv, dict) else 'not a dict'}")
print(f"OHLCV sample: {str(ohlcv)[:400]}")