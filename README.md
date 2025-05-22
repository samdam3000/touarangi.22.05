# Touarangi Engine 22.05

Touarangi is a real-time language-based sports prediction engine. It monitors live blogs, interprets predictive phrases, validates odds, and outputs actionable betting triggers to Discord and Google Docs.

---

## ⚡ Core Features

- **Live Blog Scanning** (via RSS)
- **Strike Detection**:
  - Momentum Triggers
  - Set Winner Predictions
  - Correct Score Forecasts
  - Over/Under Detection
- **Live Odds Verification** (Bet365-compatible)
- **Multi-Strike Combo Builder**
- **Google Docs Integration**
- **Discord Push Notifications**
- **JSON Logging (`strikes_log.json`, `debug_odds.json`)**

---

## 🚀 Deployment (Render)

1. **Repo Structure**: Flat file and module-compatible  
2. **Render Service Type**: `Background Worker`
3. **Start Command**:
   ```bash
   python main.py