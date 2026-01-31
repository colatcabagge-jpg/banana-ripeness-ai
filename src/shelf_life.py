def estimate_shelf_life(label: str, confidence: float):
    """
    Estimate remaining shelf life (in days) based on
    predicted class and confidence.

    Returns:
        days_left (float)
        advice (str)
    """

    label = label.lower()

    base_rules = {
        "unripe": {
            "days": 5,
            "advice": "Store at room temperature. Do not refrigerate."
        },
        "ripe": {
            "days": 2,
            "advice": "Consume soon or refrigerate to slow ripening."
        },
        "overripe": {
            "days": 1,
            "advice": "Use immediately for smoothies or baking."
        },
        "rotten": {
            "days": 0,
            "advice": "Discard. Not safe for consumption."
        }
    }

    if label not in base_rules:
        return 0, "Unknown ripeness stage."

    base_days = base_rules[label]["days"]

    # Conservative adjustment
    adjusted_days = round(base_days * confidence, 2)

    return adjusted_days, base_rules[label]["advice"]
