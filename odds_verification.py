def verify_strikes_with_odds(strike):
    try:
        # Basic confidence scoring based on phrase + odds pattern
        if 'confidence' not in strike:
            strike['confidence'] = 70  # default

        if 'odds' not in strike or strike['odds'] is None:
            strike['odds'] = 2.75

        # Simple pass-through filter
        if strike['confidence'] >= 60 and strike['odds'] <= 4.0:
            return strike
        else:
            print("[REJECTED STRIKE] Low confidence or high odds:", strike)
            return None

    except Exception as e:
        print("[VERIFY ERROR]", e)
        return None