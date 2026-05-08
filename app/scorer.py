def score_token(overview: dict) -> dict:
    """
    Enhanced risk scorer — 7 signals, 0-100 score.
    Returns score, risk_label, verdict, verdict_color, and flags.
    """
    score = 0
    flags = []

    # --- SIGNAL 1: LIQUIDITY ---
    liquidity = overview.get("liquidity", 0) or 0
    if liquidity < 1000:
        score += 25
        flags.append(("🚨", "Extremely low liquidity", f"${liquidity:,.0f} — price is trivially easy to manipulate"))
    elif liquidity < 10000:
        score += 12
        flags.append(("⚠️", "Low liquidity", f"${liquidity:,.0f} — moderate manipulation risk"))

    # --- SIGNAL 2: VOLUME vs MARKET CAP ---
    volume_24h = overview.get("v24hUSD", 0) or 0
    market_cap = overview.get("mc", 0) or 0
    if market_cap and volume_24h:
        ratio = volume_24h / market_cap
        if ratio > 10:
            score += 25
            flags.append(("🚨", "Extreme volume anomaly", f"Volume is {ratio:.1f}x market cap — coordinated pump signal"))
        elif ratio > 5:
            score += 15
            flags.append(("⚠️", "High volume anomaly", f"Volume is {ratio:.1f}x market cap — unusual activity"))
        elif ratio > 2:
            score += 8
            flags.append(("⚠️", "Elevated volume", f"Volume is {ratio:.1f}x market cap — worth monitoring"))

    # --- SIGNAL 3: PRICE SPIKE ---
    price_change = overview.get("priceChange24hPercent", 0) or \
                   overview.get("v24hChangePercent", 0) or 0
    if price_change > 500:
        score += 20
        flags.append(("🚨", "Extreme price spike", f"+{price_change:.0f}% in 24h — likely coordinated pump"))
    elif price_change > 200:
        score += 12
        flags.append(("⚠️", "Major price spike", f"+{price_change:.0f}% in 24h — high volatility"))
    elif price_change < -60:
        score += 15
        flags.append(("🚨", "Sharp price drop", f"{price_change:.0f}% in 24h — possible rug pull in progress"))

    # --- SIGNAL 4: HOLDER COUNT ---
    holders = overview.get("holder", 0) or 0
    if holders < 50:
        score += 20
        flags.append(("🚨", "Dangerously few holders", f"Only {holders} wallets hold this token"))
    elif holders < 200:
        score += 10
        flags.append(("⚠️", "Low holder count", f"Only {holders} holders — concentrated ownership"))

    # --- SIGNAL 5: WASH TRADING ---
    trades_24h = overview.get("trade24h", 0) or 0
    if volume_24h > 100000 and trades_24h < 20:
        score += 15
        flags.append(("🚨", "Wash trading detected", f"${volume_24h:,.0f} volume across only {trades_24h} trades"))

    # --- SIGNAL 6: UNIQUE WALLETS ---
    unique_wallets = overview.get("uniqueWallet24h", 0) or 0
    if unique_wallets < 10 and volume_24h > 10000:
        score += 10
        flags.append(("⚠️", "Coordinated wallet activity", f"Only {unique_wallets} unique wallets driving volume"))

    # --- SIGNAL 7: ZERO MARKET CAP ---
    if market_cap == 0 and volume_24h > 0:
        score += 5
        flags.append(("⚠️", "No market cap data", "Token supply or price data is incomplete"))

    score = min(score, 100)

    # --- RISK LABEL ---
    if score >= 70:
        risk_label = "HIGH RISK"
        risk_color = "red"
    elif score >= 40:
        risk_label = "MEDIUM RISK"
        risk_color = "yellow"
    else:
        risk_label = "LOW RISK"
        risk_color = "green"

    # --- PLAIN ENGLISH VERDICT ---
    if score >= 70:
        verdict = "AVOID — This token has multiple serious red flags consistent with a scam or pump-and-dump scheme. Do not invest."
        verdict_color = "red"
    elif score >= 40:
        verdict = "CAUTION — Some concerning signals detected. Research thoroughly and only invest what you can afford to lose entirely."
        verdict_color = "yellow"
    else:
        verdict = "LOOKS SAFE — No major red flags detected. Standard investment risks still apply — always do your own research."
        verdict_color = "green"

    return {
        "score": score,
        "risk_label": risk_label,
        "risk_color": risk_color,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "flags": flags if flags else [("✅", "No red flags", "No major risk signals detected")]
    }