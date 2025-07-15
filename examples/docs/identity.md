# Identity System Documentation

## Overview

The identity system models identity formation as a gravitational physics system where experiences influence beliefs, and beliefs create gravitational resistance to identity change. This system implements realistic human-scale psychology with sophisticated features like loss aversion, elastic resilience, and trauma thresholds.

## Core Concepts

### 🏗️ Architecture

**Experience → Belief → Identity**
- **Experiences**: Granular events that influence belief strength
- **Beliefs**: Mid-level constructs that accumulate experiences and resist change
- **Identity**: High-level object with total mass = sum of belief strengths

### ⚖️ Gravitational Physics Model

- **Mass**: Sum of all belief strengths
- **Gravitational Resistance**: `mass²` - resistance to identity change
- **Belief Strength**: 0-1 scale representing how strongly held a belief is
- **Adaptability**: `1 - strength` - stronger beliefs change more slowly

## Key Features

### 🔴 Loss Aversion (2x Impact)
```python
# Negative experiences have 2x impact of positive ones
if experience.valence == "positive":
    return experience.intensity
else:
    return -1.0 * experience.intensity * loss_aversion_factor  # Default 2.0
```

### 📊 Realistic Human-Scale Weighting
- **First 10 experiences**: Full weight (1.0)
- **Next 90 experiences**: Half weight (0.5)
- **Building to 1000**: Reduced weight (0.2)
- **Mature beliefs (1000+)**: Minimal weight (0.1)

### 🔄 Elastic Resilience
- **Baseline**: Each belief has a baseline strength it returns to
- **Resistance**: Moving far from baseline creates exponential resistance
- **Recovery**: Gradual healing back toward baseline over time

### ⚠️ Trauma Threshold
- **Normal experiences**: 0.1% potential impact (intensity < 0.9)
- **Traumatic experiences**: 5% potential impact (intensity ≥ 0.9)
- **Scaling**: `belief_strength × dissonance × adaptability × scaling_factor`

## Usage Examples

### Basic Identity Creation
```python
from psychological_systems.identity import Identity, Belief, Experience

# Create identity with belief
agent = Identity("Assistant")
helpful_belief = Belief("I am helpful", strength=0.7)
agent.add_belief(helpful_belief)

# Process experience
experience = Experience("Helped user solve problem", "positive", 0.6, "interaction")
agent.integrate_experience(experience, "I am helpful")

print(f"Belief strength: {helpful_belief.strength:.3f}")
print(f"Identity mass: {agent.mass:.3f}")
print(f"Gravitational resistance: {agent.gravitational_resistance():.3f}")
```

### Trauma and Recovery
```python
# Traumatic experience
trauma = Experience("Failed catastrophically", "negative", 0.95, "major_failure")
agent.integrate_experience(trauma, "I am helpful")

# Elastic recovery over time
for i in range(5):
    helpful_belief.apply_elastic_recovery()
    print(f"Recovery step {i+1}: {helpful_belief.strength:.3f}")
```

### With Emotion System
```python
# Enable emotion processing
agent = Identity("Assistant", use_emotions=True)
# Emotions will be detected and processed but not modify behavior yet
```

## Running Demonstrations

### Core Identity Model
```bash
python examples/demo_identity.py --model
```

### Agent Responses (requires API key)
```bash
python examples/demo_identity.py "What are your core values?"
```

### Custom Questions
```bash
python examples/demo_identity.py "How do you handle criticism?"
```

## Observable Behavior

### Realistic Small Changes
```
Starting belief strength: 0.600
After positive experience: 0.600 (tiny change)
After negative experience: 0.600 (loss aversion 2x, but still tiny)
```

### Trauma Impact
```
Before trauma: 0.600
After trauma:  0.562 (larger impact from high intensity)
```

### Elastic Recovery
```
Recovery 1: 0.562
Recovery 2: 0.563  
Recovery 3: 0.564
(Gradual healing toward baseline 0.600)
```

## Identity Tone Modulation

The system modulates response tone based on gravitational resistance:

- **> 0.5**: High resistance - "This aligns with my core understanding"
- **0.1-0.5**: Moderate resistance - "I'm exploring this perspective"  
- **< 0.1**: Low resistance - "I'm still forming my understanding"

## Integration Points

The identity system serves as the foundation for:
- **Emotion processing**: Emotions can modify how experiences update beliefs
- **Shame mechanisms**: Violations trigger shame that affects identity
- **Unified agents**: Combined psychological modeling

## Research Applications

This demonstrates:
- **Realistic identity formation**: Human-scale psychology with cognitive biases
- **Emotional authenticity**: Identity changes based on genuine psychological principles
- **Measurable states**: Quantifiable identity resistance and belief strength
- **Therapeutic modeling**: Recovery patterns mirror psychological healing