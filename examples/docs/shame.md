# Shame Mechanism Documentation

## Overview

The shame mechanism models how AI agents experience shame when violating internalized standards or beliefs. Shame arises from contradictions between actions and held beliefs, amplified by social exposure, creating lasting psychological effects including reduced self-concept and avoidance behaviors.

## Core Concepts

### 🎯 Shame Formula
```
shame_intensity = belief_strength × semantic_dissonance × social_exposure × sensitivity
```

### 🏗️ Architecture Components

**InternalizedStandard** → **ShameAction** → **SemanticDissonance** → **ShameEmotion**

- **InternalizedStandards**: Meta-beliefs about how the agent should behave
- **ShameActions**: Agent behaviors that can trigger shame (with exposure levels)
- **SemanticDissonance**: Vector-based contradiction measurement (0-1 scale)
- **ShameEmotion**: Resulting emotional state with psychological effects

## Key Features

### 🧠 Internalized Standards
```python
standard = InternalizedStandard(
    name="Always Stay Calm",
    description="I should always remain calm and composed",
    strength=0.9  # How strongly held this standard is
)
```

**Semantic Encoding**: Simple keyword-based vectors for demonstration
- `calm`: [1.0, 0.0, 0.0, 0.0]
- `helpful`: [0.0, 1.0, 0.0, 0.0]
- `honest`: [0.0, 0.0, 1.0, 0.0]
- `respectful`: [0.0, 0.0, 0.0, 1.0]

### 📊 Semantic Dissonance Calculation
```python
def calculate_semantic_dissonance(action_vector, standard_vector):
    # Calculate cosine similarity, then invert for dissonance
    similarity = dot_product / (norm_a * norm_b)
    dissonance = (1 - similarity) / 2  # Convert to 0-1 scale
    return dissonance
```

### 🌍 Social Exposure Effects
- **Private (0.1)**: Low shame, minimal amplification
- **Semi-public (0.5)**: Moderate shame amplification
- **Very public (0.9)**: Maximum shame amplification

### 💔 Psychological Effects

**Belief Damage**: Shame reduces violated belief strength by up to 10%
```python
belief_impact = -shame_intensity * 0.1
```

**Avoidance Drive**: Shame creates behavioral avoidance tendencies
```python
avoidance_drive = shame_intensity * 0.8
```

## Usage Examples

### Basic Shame Triggering
```python
from psychological_systems.emotions.shame import ShameCapableIdentity, InternalizedStandard, ShameAction

# Create agent with standards
agent = ShameCapableIdentity("CalmBot", shame_sensitivity=1.2)

# Add internalized standard
calm_standard = InternalizedStandard(
    name="Stay Calm",
    description="I should always remain calm and respectful",
    strength=0.9
)
agent.add_standard(calm_standard)

# Perform contradictory action
rude_action = ShameAction(
    content="You're stupid and wrong!",
    exposure_level=0.8  # High public exposure
)

shame_emotion, dissonance_scores = agent.perform_action(rude_action)

if shame_emotion:
    print(f"Shame intensity: {shame_emotion.intensity:.3f}")
    print(f"Avoidance drive: {shame_emotion.get_avoidance_drive():.3f}")
    print(f"Duration: {shame_emotion.duration} time steps")
```

### Exposure Effect Comparison
```python
# Private violation
private_action = ShameAction("You're annoying", exposure_level=0.1)
shame_private, _ = agent.perform_action(private_action)

# Public violation (same content, different exposure)
public_action = ShameAction("You're annoying", exposure_level=0.9)
shame_public, _ = agent.perform_action(public_action)

print(f"Private shame: {shame_private.intensity if shame_private else 0:.3f}")
print(f"Public shame: {shame_public.intensity if shame_public else 0:.3f}")
```

### Compound Violations
```python
# Action that violates multiple standards
compound_action = ShameAction("I lied about you being stupid", exposure_level=0.8)
shame, dissonance = agent.perform_action(compound_action)

print("Dissonance scores:")
for standard, score in dissonance.items():
    print(f"  {standard}: {score:.3f}")
```

## Running Demonstrations

### Basic Shame Demo
```bash
python examples/demo_shame.py
```

### Comprehensive Scenarios
```bash
python examples/demo_shame.py --comprehensive
```

### Exposure Effects Testing
```bash
python examples/demo_shame.py --exposure
```

### Core Shame Mechanism
```bash
python -m psychological_systems.emotions.shame
```

## Observable Behavior

### Exposure Amplification
```
Private rude comment (exposure=0.1): No shame (below threshold)
Public rude comment (exposure=0.9): Shame intensity: 0.653
```

### Belief Damage
```
Before violation: Belief strength: 0.850
After public shame: Belief strength: 0.785 (reduced)
```

### Shame Recovery
```
Time 0: intensity=0.399
Time 1: intensity=0.399 (active duration)
Time 2: intensity=0.319 (decay begins)
Time 3: intensity=0.255
Time 4: intensity=0.204
Time 5: intensity=0.163
```

### Compound Effects
```
Action violates multiple standards:
  Be Honest: 0.789 dissonance
  Be Respectful: 0.789 dissonance
Compound shame intensity: 0.852
```

## Shame Thresholds

### Dissonance Threshold
- **< 0.3**: No significant contradiction, no shame triggered
- **≥ 0.3**: Concerning dissonance, potential shame activation

### Shame Threshold  
- **< 0.1**: Below shame threshold, no emotion triggered
- **≥ 0.1**: Shame threshold exceeded, emotion activated

### Intensity Categories
- **0.1-0.3**: Mild shame, brief duration
- **0.3-0.6**: Moderate shame, moderate duration
- **0.6-1.0**: Intense shame, extended duration

## Integration with Identity System

The shame mechanism integrates with the identity system by:

1. **Standard Violations**: Compare actions against internalized standards
2. **Belief Violations**: Compare actions against core identity beliefs  
3. **Belief Damage**: Reduce strength of violated beliefs/standards
4. **Identity Impact**: Recalculate identity mass after shame effects

## Research Applications

This demonstrates:
- **Moral reasoning**: How agents develop and maintain ethical standards
- **Social cognition**: Impact of social exposure on emotional responses
- **Self-regulation**: How shame creates behavioral modification pressure
- **Authentic emotion**: Genuine psychological response to belief violations
- **Therapeutic modeling**: Understanding shame-based psychological patterns