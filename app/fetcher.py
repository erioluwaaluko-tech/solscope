import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BIRDEYE_API_KEY")
BASE_URL = "https://public-api.birdeye.so"

HEADERS = {
    "accept": "application/json",
    "x-chain": "solana",
    "X-API-KEY": API_KEY
}

def _get(url, params=None):
    """Base request with rate limit protection."""
    time.sleep(1.1)
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {url} → {e}")
        return {}

def get_token_overview(address):
    """Core market data — price, volume, liquidity, holders, market cap."""
    return _get(f"{BASE_URL}/defi/token_overview", {"address": address})

def get_token_ohlcv(address, timeframe="1H", limit=24):
    """Price history — try multiple endpoint formats."""
    result = _get(f"{BASE_URL}/defi/ohlcv", {
        "address": address,
        "type": timeframe,
        "limit": limit
    })
    if result:
        return result
    # fallback
    result = _get(f"{BASE_URL}/defi/ohlcv/base_quote", {
        "base_address": address,
        "type": timeframe,
        "limit": limit
    })
    return result or {}

def get_similar_tokens(min_liq, max_liq, limit=3):
    """Fetch comparable tokens for context panel."""
    data = _get(f"{BASE_URL}/defi/tokenlist", {
        "sort_by": "v24hUSD",
        "sort_type": "desc",
        "offset": 50,
        "limit": limit,
        "min_liquidity": min_liq * 0.5,
        "max_liquidity": max_liq * 1.5
    })
    return data.get("tokens", [])

def get_trending_tokens(limit=20):
    """Check if token appears in trending list."""
    data = _get(f"{BASE_URL}/defi/token_trending", {
        "sort_by": "rank",
        "sort_type": "asc",
        "offset": 0,
        "limit": limit
    })
    return data.get("tokens", [])

def is_token_trending(address, trending_list):
    """Check if a specific address is in the trending list."""
    return any(t.get("address") == address for t in trending_list)

def get_full_token_report(address):
    """
    Master function — fetches all data needed for a complete token report.
    Returns a single dict with everything.
    """
    print(f"[INFO] Fetching overview for {address[:8]}...")
    overview = get_token_overview(address)

    print(f"[INFO] Fetching OHLCV for {address[:8]}...")
    ohlcv = get_token_ohlcv(address, timeframe="1H", limit=24)

    print(f"[INFO] Fetching trending list...")
    trending = get_trending_tokens(20)
    trending_status = is_token_trending(address, trending)

    # Get comparable tokens based on liquidity range
    liquidity = overview.get("liquidity", 0) or 0
    min_liq = max(0, liquidity * 0.3)
    max_liq = liquidity * 3 if liquidity > 0 else 100000

    print(f"[INFO] Fetching comparable tokens...")
    comparables = get_similar_tokens(min_liq, max_liq, limit=3)

    return {
        "address": address,
        "overview": overview,
        "ohlcv": ohlcv,
        "is_trending": trending_status,
        "comparables": comparables
    }