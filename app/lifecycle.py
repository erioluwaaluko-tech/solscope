def classify_lifecycle(overview: dict, ohlcv: dict) -> dict:
    """
    Classify where a token is in its market lifecycle.
    Uses price momentum, volume trend, and holder velocity.

    Stages:
    - EARLY       : New token, low activity, unknown trajectory
    - GROWING     : Rising holders, organic volume increase, best entry window
    - PEAKING     : Volume at highs, price spiking, momentum buying
    - DISTRIBUTION: Price stalling, volume still high, whales selling to retail
    - DECLINING   : Volume falling, price dropping, interest fading
    """

    stage = "UNKNOWN"
    confidence = "LOW"
    explanation = ""
    color = "gray"

    # --- Extract signals ---
    price_change_24h = overview.get("priceChange24hPercent", 0) or \
                       overview.get("v24hChangePercent", 0) or 0
    volume_24h = overview.get("v24hUSD", 0) or overview.get("v24h", 0) or 0
    holders = overview.get("holder", 0) or 0
    liquidity = overview.get("liquidity", 0) or 0
    market_cap = overview.get("marketCap", 0) or overview.get("mc", 0) or 0
    unique_wallets = overview.get("uniqueWallet24h", 0) or 0
    trades_24h = overview.get("trade24h", 0) or 0

    # --- OHLCV trend analysis ---
    items = []
    if isinstance(ohlcv, dict):
        items = ohlcv.get("items", [])
    elif isinstance(ohlcv, list):
        items = ohlcv

    volume_trend = "flat"
    price_trend = "flat"

    if len(items) >= 6:
        # Compare first half vs second half volume
        mid = len(items) // 2
        early_vol = sum(c.get("v", 0) or 0 for c in items[:mid])
        late_vol  = sum(c.get("v", 0) or 0 for c in items[mid:])
        if late_vol > early_vol * 1.5:
            volume_trend = "rising"
        elif late_vol < early_vol * 0.6:
            volume_trend = "falling"

        # Price trend from first to last candle
        first_close = items[0].get("c",  0) or 0
        last_close  = items[-1].get("c", 0) or 0
        if first_close and last_close:
            price_move = ((last_close - first_close) / first_close) * 100
            if price_move > 20:
                price_trend = "rising"
            elif price_move < -20:
                price_trend = "falling"

    # --- Volume / MarketCap ratio ---
    vol_mcap_ratio = (volume_24h / market_cap) if market_cap else 0

    # --- Classification logic ---
    if holders < 100 and volume_24h < 50000:
        stage = "EARLY"
        confidence = "HIGH"
        color = "blue"
        explanation = (
            "This token is in its earliest stage — very few holders and low volume. "
            "It could be a legitimate new launch or a pre-pump setup. "
            "Highest risk but also highest potential upside if genuine."
        )

    elif volume_trend == "rising" and price_trend == "rising" and price_change_24h < 200:
        stage = "GROWING"
        confidence = "HIGH"
        color = "green"
        explanation = (
            "Volume and price are both trending up organically. "
            "Holder count is building. This is typically the best entry window "
            "for traders — momentum is building but the big move hasn't happened yet."
        )

    elif price_change_24h > 200 or vol_mcap_ratio > 5:
        stage = "PEAKING"
        confidence = "HIGH"
        color = "yellow"
        explanation = (
            "This token has already made a significant move. "
            "Volume is extremely high relative to market cap. "
            "Late buyers at this stage are typically buying from early holders who are selling. "
            "Proceed with extreme caution."
        )

    elif price_change_24h > 50 and volume_trend == "falling":
        stage = "DISTRIBUTION"
        confidence = "MEDIUM"
        color = "orange"
        explanation = (
            "Price is elevated but volume is starting to fade. "
            "This is the distribution phase — early buyers are selling their positions "
            "to late buyers attracted by the recent price move. Classic dump setup."
        )

    elif price_trend == "falling" and volume_trend == "falling":
        stage = "DECLINING"
        confidence = "HIGH"
        color = "red"
        explanation = (
            "Both price and volume are falling. Interest in this token is fading. "
            "Unless there is a strong catalyst, this trend typically continues. "
            "High risk of further downside."
        )

    else:
        stage = "CONSOLIDATING"
        confidence = "LOW"
        color = "gray"
        explanation = (
            "This token does not show a clear directional trend. "
            "Volume and price are relatively stable. "
            "Could break either way — watch for volume spikes as early signals."
        )

    return {
        "stage": stage,
        "confidence": confidence,
        "color": color,
        "explanation": explanation,
        "signals": {
            "price_change_24h": price_change_24h,
            "volume_trend": volume_trend,
            "price_trend": price_trend,
            "vol_mcap_ratio": round(vol_mcap_ratio, 2),
            "holders": holders,
            "unique_wallets_24h": unique_wallets,
        }
    }
