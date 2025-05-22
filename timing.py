# timing.py

from datetime import datetime, timedelta

def get_utc_time():
    """
    Returns the current UTC time as a datetime object.
    """
    return datetime.utcnow()

def get_match_minute(start_time):
    """
    Calculates current match minute based on provided start_time (UTC datetime).
    """
    now = datetime.utcnow()
    elapsed = now - start_time
    return int(elapsed.total_seconds() // 60)

def format_utc(dt=None):
    """
    Returns a UTC timestamp as a formatted string. Defaults to now.
    """
    if not dt:
        dt = datetime.utcnow()
    return dt.strftime("%H:%M:%S UTC")

def get_game_phase(minute):
    """
    Converts a match minute into a labeled game phase (early/mid/late).
    """
    if minute < 20:
        return "early"
    elif 20 <= minute <= 60:
        return "mid"
    else:
        return "late"

def minutes_since(timestamp):
    """
    Returns how many minutes have passed since a given UTC datetime object.
    """
    now = datetime.utcnow()
    return int((now - timestamp).total_seconds() / 60)

def utc_to_local(utc_time, offset_hours=0):
    """
    Converts UTC time to local time using offset (e.g., +12 for NZST).
    """
    return utc_time + timedelta(hours=offset_hours)