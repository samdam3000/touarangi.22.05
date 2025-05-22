import time
import requests
from datetime import datetime
from main_diagnostic import run_engine

def cron_loop():
    print("[CRON] Touarangi Cron started at", datetime.utcnow().isoformat())
    while True:
        try:
            print("[CRON] Triggering run_engine at", datetime.utcnow().isoformat())
            run_engine()
        except Exception as e:
            print("[CRON ERROR]", e)
        time.sleep(30)

if __name__ == "__main__":
    cron_loop()
