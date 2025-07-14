import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_entropy(logits):
    # Normalize logits if needed
    probs = np.exp(logits) / np.sum(np.exp(logits))
    entropy = -np.sum(probs * np.log(probs + 1e-9))
    return entropy  # Float value

def get_embedding(text: str):
    """Get embedding for a text using OpenAI's text-embedding-ada-002"""
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def score_similarity_variance(outputs: list[str]):
    """Calculate uncertainty based on semantic similarity variance"""
    if len(outputs) < 2:
        return 0.0
    
    # Get embeddings for all outputs
    embeddings = []
    for output in outputs:
        emb = get_embedding(output)
        if emb is not None:
            embeddings.append(emb)
    
    if len(embeddings) < 2:
        # Fallback to hash method if embeddings fail
        return score_variance_hash(outputs)
    
    # Calculate pairwise similarities
    embeddings = np.array(embeddings)
    similarities = cosine_similarity(embeddings)
    
    # Get upper triangle (excluding diagonal)
    n = len(similarities)
    upper_triangle = similarities[np.triu_indices(n, k=1)]
    
    # High similarity = low uncertainty, so invert
    avg_similarity = np.mean(upper_triangle)
    uncertainty = 1.0 - avg_similarity  # Convert to uncertainty score
    
    return uncertainty

def score_variance_hash(outputs: list[str]):
    """Original hash-based variance scoring (fallback method)"""
    return np.std([hash(o) for o in outputs]) / 10000

def score_variance(outputs: list[str], method="similarity"):
    """Score uncertainty using specified method"""
    if method == "similarity":
        return score_similarity_variance(outputs)
    elif method == "hash":
        return score_variance_hash(outputs)
    else:
        # Try similarity first, fallback to hash
        try:
            return score_similarity_variance(outputs)
        except:
            return score_variance_hash(outputs)
