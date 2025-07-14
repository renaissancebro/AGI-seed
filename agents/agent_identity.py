from core.identity_model import Identity, Belief, Experience
from core.verbalizer import identity_tone
from models.models import run_model

def respond(prompt: str):
    """
    Agent response using gravitational identity model.
    
    Creates multiple responses, calculates identity consistency through
    gravitational resistance, and applies appropriate identity tone.
    """
    outputs = run_model(prompt, n_samples=3)
    
    # Create temporary identity to measure response consistency
    temp_identity = Identity("temp_agent")
    response_belief = Belief("response_consistency", strength=0.5)
    temp_identity.add_belief(response_belief)
    
    # Convert responses to experiences and measure gravitational resistance
    for i, output in enumerate(outputs):
        # Simulate experience based on response similarity
        # More consistent responses = stronger positive experiences
        experience = Experience(
            content=output[:50] + "...",  # Truncate for content
            valence="positive" if len(output) > 10 else "negative", 
            intensity=min(len(output) / 100.0, 1.0),  # Length as proxy for coherence
            source=f"response_{i}"
        )
        temp_identity.integrate_experience(experience, "response_consistency")
    
    # Use gravitational resistance as identity stability score
    gravity_score = temp_identity.gravitational_resistance()
    final_output = outputs[0]  # Pick first response for display
    
    return identity_tone(final_output, gravity_score)