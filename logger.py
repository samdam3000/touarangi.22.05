# logger.py

import logging
from datetime import datetime

# Configure global logger
logging.basicConfig(
    filename="touarangi.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

def log_info(message):
    """
    Logs a general info-level message to console and file.
    """
    print(f"[INFO] {message}")
    logging.info(message)

def log_warning(message):
    """
    Logs a warning-level message.
    """
    print(f"[WARN] {message}")
    logging.warning(message)

def log_error(message):
    """
    Logs an error-level message.
    """
    print(f"[ERROR] {message}")
    logging.error(message)

def log_strike_summary(strike):
    """
    Logs a formatted strike dictionary to the log file.
    """
    msg = (
        f"STRIKE | {strike.get('market')} | {strike.get('player')} | "
        f"Conf: {strike.get('confidence')}% | Odds: {strike.get('odds')} | "
        f"Reason: {strike.get('reason')}"
    )
    log_info(msg)

def log_system_start():
    log_info("Touarangi Engine started at " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

def log_cycle_complete():
    log_info("Cycle complete at " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))