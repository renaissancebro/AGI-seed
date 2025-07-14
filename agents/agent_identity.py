from core.physics_model import calculate_gravity_influence
from core.verbalizer import identity_tone
from models.models import run_model

def respond(prompt: str):
    outputs = run_model(prompt, n_samples=3)
    gravity_score = calculate_gravity_influence(outputs)
    final_output = outputs[0]  # just pick one for display
    return identity_tone(final_output, gravity_score)