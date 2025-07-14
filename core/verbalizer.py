def uncertainty_tone(output: str, score: float) -> str:
    if score < 0.2:
        return output
    elif score < 0.5:
        return "I believe this is likely, but not fully certain:\n" + output
    else:
        return "This may be unreliable — here's my best attempt:\n" + output
