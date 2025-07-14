import numpy as np

def score_entropy(logits):
    # Normalize logits if needed
    probs = np.exp(logits) / np.sum(np.exp(logits))
    entropy = -np.sum(probs * np.log(probs + 1e-9))
    return entropy  # Float value

def score_variance(outputs: list[str]):
    # Use simple token-level or embedding-level diff
    return np.std([hash(o) for o in outputs]) / 10000
