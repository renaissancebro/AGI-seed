def uncertainty_tone(output: str, score: float) -> str:
    if score < 0.1:
        return output  # Fully confident
    elif score < 0.5:
        return "I think this is likely, but not fully certain:\n" + output
    else:
        return "This may be unreliable — here's my best attempt:\n" + output
