from core.uncertainty_model import score_variance
from core.verbalizer import uncertainty_tone
from models.models import run_model

def respond(prompt: str):
    outputs = run_model(prompt, n_samples=3)
    score = score_variance(outputs)
    final_output = outputs[0]  # just pick one for display
    return uncertainty_tone(final_output, score)
