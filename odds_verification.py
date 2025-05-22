
def verify_strikes_with_odds(strike):
    try:
        if 'confidence' not in strike:
            strike['confidence'] = 70

        if 'odds' not in strike or strike['odds'] is None:
            strike['odds'] = 2.75

        if strike['player'] == "Unknown":
            print("[REJECTED] No player found in strike:", strike)
            return None

        if strike['confidence'] >= 60 and strike['odds'] <= 4.0:
            return strike
        else:
            print("[REJECTED] Odds/confidence too low:", strike)
            return None

    except Exception as e:
        print("[VERIFY ERROR]", e)
        return None
