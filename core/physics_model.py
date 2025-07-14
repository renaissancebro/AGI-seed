"""
Physics-based identity modeling using gravity and object interactions.
Models identity formation through gravitational forces between concepts.
"""

import difflib

def calculate_gravity_influence(responses: list) -> float:
    """
    Calculate identity gravity score based on response consistency.
    
    Uses physics metaphor where:
    - Consistent responses = strong gravitational pull (stable identity)
    - Inconsistent responses = weak gravity (fluid/forming identity)
    
    Returns score between 0-1:
    - High score (>0.7): Strong identity gravity (consistent self-concept)
    - Medium score (0.3-0.7): Moderate identity gravity (some fluidity)
    - Low score (<0.3): Weak identity gravity (highly adaptive/uncertain identity)
    """
    if len(responses) < 2:
        return 0.5  # neutral gravity when insufficient data
    
    # Calculate pairwise similarity using gravitational metaphor
    similarities = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            similarity = difflib.SequenceMatcher(None, responses[i], responses[j]).ratio()
            similarities.append(similarity)
    
    # Average similarity represents gravitational strength
    avg_similarity = sum(similarities) / len(similarities)
    
    # Invert to match gravity metaphor (high consistency = strong gravity)
    gravity_score = avg_similarity
    
    return gravity_score

def calculate_object_mass(response_length: int) -> float:
    """
    Calculate conceptual 'mass' of a response.
    Longer, more detailed responses have higher conceptual mass.
    """
    return min(response_length / 100.0, 1.0)  # normalized to 0-1

def simulate_identity_orbit(responses: list) -> dict:
    """
    Simulate orbital mechanics of identity concepts.
    Returns orbital characteristics representing identity stability.
    """
    gravity = calculate_gravity_influence(responses)
    masses = [calculate_object_mass(len(r)) for r in responses]
    
    # Stable orbit = consistent identity
    # Elliptical orbit = variable identity
    # Escape velocity = identity crisis
    
    orbital_stability = gravity * (sum(masses) / len(masses))
    
    return {
        "gravity_strength": gravity,
        "orbital_stability": orbital_stability,
        "identity_coherence": min(orbital_stability * 1.2, 1.0)
    }