from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.fetcher import get_full_token_report
from app.scorer import score_token
from app.lifecycle import classify_lifecycle
import time

app = FastAPI(
    title="SolScope",
    description="Token Intelligence Terminal for Solana",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    html_path = Path(__file__).parent.parent / "dashboard.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return {"status": "online", "message": "SolScope is running"}

def build_chart_from_overview(overview: dict) -> list:
    """
    Build a price chart from overview history fields
    when OHLCV endpoint returns no data.
    Uses the price snapshots available in token_overview.
    """
    import time as t
    now = int(t.time())
    price = overview.get("price", 0) or 0

    points = [
        {"label": "24h ago", "offset": 86400, "key": "history24hPrice"},
        {"label": "8h ago",  "offset": 28800, "key": "history8hPrice"},
        {"label": "4h ago",  "offset": 14400, "key": "history4hPrice"},
        {"label": "2h ago",  "offset": 7200,  "key": "history2hPrice"},
        {"label": "1h ago",  "offset": 3600,  "key": "history1hPrice"},
        {"label": "Now",     "offset": 0,     "key": "price"},
    ]

    chart = []
    for p in points:
        val = overview.get(p["key"], 0) or 0
        if val:
            chart.append({
                "time": now - p["offset"],
                "open": val, "high": val, "low": val,
                "close": val, "volume": 0
            })

    return chart if len(chart) >= 2 else []

@app.get("/api/analyze/{address}")
def analyze_token(address: str):
    """Full token intelligence report."""
    try:
        report = get_full_token_report(address)
        overview = report["overview"]
        ohlcv = report["ohlcv"]

        score_result = score_token(overview)
        lifecycle_result = classify_lifecycle(overview, ohlcv)

        # Format OHLCV for chart
        items = []
        if isinstance(ohlcv, dict):
            items = ohlcv.get("items", [])
        elif isinstance(ohlcv, list):
            items = ohlcv

        chart_data = [
            {
                "time": c.get("unixTime", 0),
                "open":  c.get("o", 0),
                "high":  c.get("h", 0),
                "low":   c.get("l", 0),
                "close": c.get("c", 0),
                "volume": c.get("v", 0),
            }
            for c in items if c.get("unixTime")
        ]

        # Format flags for frontend
        formatted_flags = [
            {"icon": f[0], "title": f[1], "detail": f[2]}
            for f in score_result["flags"]
        ]

        # Format comparables
        comparables = []
        for t in report.get("comparables", []):
            comparables.append({
                "address":  t.get("address", ""),
                "symbol":   t.get("symbol", "?"),
                "name":     t.get("name", "?"),
                "price":    t.get("price", 0),
                "liquidity": t.get("liquidity", 0),
                "volume_24h": t.get("v24hUSD", 0),
                "holders":  t.get("holder", 0),
            })

        return {
            "address":      address,
            "symbol":       overview.get("symbol", "?"),
            "name":         overview.get("name", "?"),
            "logo":         overview.get("logoURI", ""),
            "price":        overview.get("price", 0),
            "price_change_24h": overview.get("priceChange24hPercent", 0) or overview.get("v24hChangePercent", 0) or 0,
            "market_cap":   overview.get("marketCap", 0) or overview.get("mc", 0) or overview.get("fdv", 0) or 0,
            "liquidity":    overview.get("liquidity", 0),
            "volume_24h":   overview.get("v24hUSD", 0),
            "holders":      overview.get("holder", 0),
            "unique_wallets_24h": overview.get("uniqueWallet24h", 0),
            "trades_24h":   overview.get("trade24h", 0),
            "is_trending":  report.get("is_trending", False),
            "risk_score":   score_result["score"],
            "risk_label":   score_result["risk_label"],
            "risk_color":   score_result["risk_color"],
            "verdict":      score_result["verdict"],
            "verdict_color": score_result["verdict_color"],
            "flags":        formatted_flags,
            "lifecycle":    lifecycle_result,
            "chart_data":   chart_data if chart_data else build_chart_from_overview(overview),
            "comparables":  comparables,
            "scanned_at":   time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    except Exception as e:
        return {"error": str(e), "address": address}

@app.get("/status")
def status():
    return {"status": "online", "message": "SolScope Token Intelligence Terminal"}