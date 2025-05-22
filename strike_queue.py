# strike_queue.py

from datetime import datetime, timedelta

# In-memory list of recent confirmed strikes
STRIKE_HISTORY = []

def get_confirmed_strikes(within_minutes=3):
    """
    Returns all confirmed strikes within the last `within_minutes` (default: 3).
    Useful for multi-strike combos or syncing opportunities.
    """
    now = datetime.utcnow()
    return [
        strike for strike in STRIKE_HISTORY
        if "confirmed_time" in strike and (now - strike["confirmed_time"]) <= timedelta(minutes=within_minutes)
    ]

def add_strike(strike):
    """
    Adds a confirmed strike to memory history for tracking.
    Automatically prunes entries older than 10 minutes.
    """
    strike["added_time"] = datetime.utcnow()
    STRIKE_HISTORY.append(strike)
    prune_old_strikes()

def prune_old_strikes(max_age_minutes=10):
    """
    Removes strikes older than `max_age_minutes` from the queue.
    Prevents memory bloat and stale combos.
    """
    now = datetime.utcnow()
    global STRIKE_HISTORY
    STRIKE_HISTORY = [
        s for s in STRIKE_HISTORY
        if "confirmed_time" in s and (now - s["confirmed_time"]) <= timedelta(minutes=max_age_minutes)
    ]

def reset_queue():
    """
    Clears all stored strikes. Use before a new match or at halftime reset.
    """
    global STRIKE_HISTORY
    STRIKE_HISTORY = []