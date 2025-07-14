import numpy as np
from difflib import SequenceMatcher

def score_entropy(logits):
    # Normalize logits if needed
    probs = np.exp(logits) / np.sum(np.exp(logits))
    entropy = -np.sum(probs * np.log(probs + 1e-9))
    return entropy  # Float value

def string_similarity(a, b):
    """Calculate similarity between two strings using SequenceMatcher"""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def score_variance(outputs: list[str]):
    """Calculate uncertainty based on string similarity variance"""
    if len(outputs) < 2:
        return 0.0
    
    # Calculate pairwise similarities
    similarities = []
    for i in range(len(outputs)):
        for j in range(i + 1, len(outputs)):
            sim = string_similarity(outputs[i], outputs[j])
            similarities.append(sim)
    
    # High similarity = low uncertainty, so invert
    avg_similarity = np.mean(similarities)
    uncertainty = 1.0 - avg_similarity
    
    return uncertainty
