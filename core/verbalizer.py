def uncertainty_tone(output: str, score: float) -> str:
    if score < 0.1:
        return output  # Fully confident
    elif score < 0.5:
        return "I think this is likely, but not fully certain:\n" + output
    else:
        return "This may be unreliable — here's my best attempt:\n" + output

def identity_tone(output: str, gravity_score: float) -> str:
    """
    Apply identity-based tone modulation using gravitational resistance.
    
    High gravitational resistance = stable, consistent identity
    Low gravitational resistance = fluid, adaptive identity
    """
    if gravity_score > 0.5:
        # High gravitational resistance - stable identity
        return f"This aligns with my core understanding:\n{output}"
    elif gravity_score > 0.1:
        # Moderate resistance - some identity fluidity
        return f"I'm exploring this perspective:\n{output}"
    else:
        # Low resistance - forming/adaptive identity
        return f"I'm still forming my understanding of this:\n{output}"
