# 🔭 SolScope — Token Intelligence Terminal

> Know before you buy. Paste any Solana token address for a complete intelligence report in seconds.

![Birdeye API](https://img.shields.io/badge/Birdeye-Data%20API-blue) ![Python](https://img.shields.io/badge/Python-3.13-green) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal) ![Sprint](https://img.shields.io/badge/BirdeyeAPI-Sprint%203-purple)

**Live:** https://solscope-i3jg.onrender.com

---

## What It Does

SolScope is a free Token Intelligence Terminal for Solana. Paste any token address and get a complete intelligence report — no wallet connection, no sign-up, no fees.

Every report includes:
- **Risk Score** (0–100) across 6 on-chain signals
- **Plain-English Verdict** — Looks Safe / Caution / Avoid
- **Lifecycle Stage** — Early / Growing / Peaking / Distribution / Declining
- **24h Price Chart** from Birdeye OHLCV data
- **Market Health** — price, volume, liquidity, holders, trades
- **Comparable Tokens** — 3 similar tokens for context
- **Copy Report** — formatted summary ready to share on Discord or Telegram

---

## Risk Scoring — 6 Signals

| Signal | Max Points | What It Detects |
|--------|-----------|-----------------|
| Liquidity depth | 25 pts | Low liquidity = easy price manipulation |
| Volume / Market Cap ratio | 25 pts | Extreme ratio = coordinated pump signal |
| 24h price spike | 20 pts | 200%+ move = possible pump in progress |
| Holder count | 20 pts | Under 50 holders = concentrated dump risk |
| Wash trading signal | 15 pts | High volume + very few trades = fake activity |
| Unique wallet activity | 10 pts | Few wallets driving high volume = coordinated buying |

**Risk Labels:** 🟢 LOW RISK (0–39) · 🟡 MEDIUM RISK (40–69) · 🔴 HIGH RISK (70–100)

---

## Lifecycle Stage Classifier

Every token sits somewhere in a market cycle. SolScope tells you exactly where:

- **Early** — New launch, few holders, unknown trajectory. Highest risk, highest potential.
- **Growing** — Volume rising organically, holder count building. Best entry window.
- **Peaking** — Price has already spiked. Late entry risk — momentum buying phase.
- **Distribution** — Price stalling, volume fading. Early holders selling to late buyers.
- **Declining** — Both price and volume falling. High risk of further downside.

---

## Tech Stack

- **Backend:** Python 3.13, FastAPI, Uvicorn
- **Data:** Birdeye Data API — `/defi/token_overview`, `/defi/ohlcv`, `/defi/token_trending`, `/defi/tokenlist`
- **Frontend:** Vanilla HTML/CSS/JS, Chart.js
- **Deployment:** Render

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Serves the SolScope dashboard |
| `GET /api/analyze/{address}` | Full intelligence report for any Solana token |
| `GET /status` | Server health check |

---

## Run Locally

```bash
git clone https://github.com/erioluwaaluko-tech/solscope.git
cd solscope
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
BIRDEYE_API_KEY=your_key_here


Start server:
```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

---

## Birdeye Endpoints Used

- `/defi/token_overview` — price, volume, liquidity, holders, market cap
- `/defi/ohlcv` — 24h price history for chart and lifecycle analysis
- `/defi/token_trending` — checks if token is currently trending
- `/defi/tokenlist` — fetches comparable tokens for context

---

## Built For

[Birdeye Data BIP Competition](https://bds.birdeye.so) — Sprint 3 (May 2–9, 2026)

Built by [@erioluwaaluko-tech](https://github.com/erioluwaaluko-tech)