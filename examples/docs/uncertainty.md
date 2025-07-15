# Uncertainty System Documentation

## Overview

The uncertainty system treats uncertainty as an AI measurement tool rather than an emotion. It measures response consistency to determine epistemic uncertainty and applies appropriate verbal qualifiers to AI responses. This system is designed for AI safety and transparency, helping users understand when AI responses may be unreliable.

## Core Concepts

### 🎯 Uncertainty as Measurement Tool
Unlike the emotion templates, uncertainty is treated as a **cognitive assessment** that:
- Measures response variance/consistency
- Indicates epistemic confidence levels  
- Drives verbal expression modulation
- Provides transparency about AI reliability

### 📊 Variance Calculation
```python
def score_variance(responses: list) -> float:
    similarities = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            similarity = difflib.SequenceMatcher(None, responses[i], responses[j]).ratio()
            similarities.append(similarity)
    
    avg_similarity = sum(similarities) / len(similarities)
    return 1.0 - avg_similarity  # High variance = high uncertainty
```

### 🗣️ Verbal Expression
The system applies tone modulation based on uncertainty scores:
- **Low uncertainty** (< 0.1): Clean response, no qualifier
- **Medium uncertainty** (0.1-0.5): "I think this is likely, but not fully certain"
- **High uncertainty** (> 0.5): "This may be unreliable — here's my best attempt"

## Key Features

### ⚖️ Response Sampling
```python
def respond(prompt: str):
    outputs = run_model(prompt, n_samples=3)  # Generate multiple responses
    score = score_variance(outputs)           # Measure consistency
    final_output = outputs[0]                 # Pick one for display
    return uncertainty_tone(final_output, score)  # Apply qualifier
```

### 🎭 Tone Application
```python
def uncertainty_tone(output: str, score: float) -> str:
    if score < 0.1:
        return output  # Fully confident
    elif score < 0.5:
        return "I think this is likely, but not fully certain:\n" + output
    else:
        return "This may be unreliable — here's my best attempt:\n" + output
```

### 📈 Question Type Sensitivity
Different question types show different uncertainty patterns:
- **Factual questions**: Low uncertainty (consistent responses)
- **Opinion questions**: Medium uncertainty (some variation)
- **Philosophical questions**: High uncertainty (high variation)

## Usage Examples

### Basic Uncertainty Measurement
```python
from core.uncertainty_model import score_variance
from core.verbalizer import uncertainty_tone

# Identical responses = low uncertainty
responses1 = ['4', '4', '4']
uncertainty1 = score_variance(responses1)
print(f"Identical responses: {uncertainty1:.3f}")  # ~0.0

# Varied responses = high uncertainty  
responses2 = ['4', 'four', 'Two plus two equals four']
uncertainty2 = score_variance(responses2)
print(f"Varied responses: {uncertainty2:.3f}")     # ~0.9

# Apply tone
response = "The answer is 4"
qualified_response = uncertainty_tone(response, uncertainty2)
print(qualified_response)
```

### Agent Integration
```python
from agents.uncertainty_agent import respond

# Requires OpenAI API key
response = respond("What is 2+2?")  # Low uncertainty expected
response = respond("What is the best programming language?")  # High uncertainty expected
response = respond("What happens after we die?")  # Very high uncertainty expected
```

### Direct Tone Testing
```python
from core.verbalizer import uncertainty_tone

# Test different uncertainty levels
print("Low (0.05):", uncertainty_tone("The answer is 4", 0.05))
print("Medium (0.3):", uncertainty_tone("Python is good", 0.3))  
print("High (0.7):", uncertainty_tone("Maybe consciousness is...", 0.7))
```

## Running Demonstrations

### Full Uncertainty Demo (requires API key)
```bash
python examples/demo_questions.py
```

### Core Measurement Testing
```python
python -c "
from core.uncertainty_model import score_variance
responses = ['identical', 'identical', 'identical']
print('Low uncertainty:', score_variance(responses))
responses = ['different', 'varied', 'responses']
print('High uncertainty:', score_variance(responses))
"
```

### Tone Application Testing
```python
python -c "
from core.verbalizer import uncertainty_tone
print(uncertainty_tone('Test response', 0.0))
print(uncertainty_tone('Test response', 0.3)) 
print(uncertainty_tone('Test response', 0.8))
"
```

## Observable Behavior

### Response Variance Examples
```
Identical responses: uncertainty = 0.0
Similar responses: uncertainty = 0.2-0.4
Varied responses: uncertainty = 0.6-0.9
Completely different: uncertainty = 0.9+
```

### Tone Modulation Examples
```
Low uncertainty (0.05): 
"The answer is 4"

Medium uncertainty (0.3):
"I think this is likely, but not fully certain:
Python is good for beginners"

High uncertainty (0.7):
"This may be unreliable — here's my best attempt:
Consciousness might be an emergent property"
```

### Question Type Patterns
```
Factual: "What is 2+2?" → Low uncertainty (0.0-0.2)
Opinion: "Best programming language?" → Medium uncertainty (0.3-0.6)
Philosophy: "What is consciousness?" → High uncertainty (0.7-1.0)
```

## Integration with Other Systems

### Conceptual Integration Example
```python
# Uncertainty can influence identity formation
uncertainty = score_variance(responses)
experience_quality = max(0.1, 1.0 - uncertainty)  # High uncertainty = poor experience

# Create experience for identity system
experience = Experience(
    content="Generated response about self",
    valence="positive" if experience_quality > 0.5 else "negative",
    intensity=experience_quality,
    source="self_reflection"
)

# Low uncertainty = positive identity experience
# High uncertainty = negative identity experience
```

### Separate from Emotions
Unlike emotions, uncertainty:
- Is **measurement-focused** rather than **behavior-modifying**
- Provides **epistemic assessment** rather than **affective response**
- Drives **transparency** rather than **psychological change**
- Serves **AI safety** rather than **emotional modeling**

## Uncertainty Thresholds

### Response Consistency
- **0.0-0.1**: Highly consistent responses (factual, mathematical)
- **0.1-0.3**: Somewhat consistent (opinions with clear consensus)
- **0.3-0.6**: Moderate variation (subjective topics)
- **0.6-0.9**: High variation (complex, philosophical topics)
- **0.9-1.0**: Completely inconsistent responses

### Confidence Levels
- **Fully confident** (< 0.1): No uncertainty qualifier needed
- **Moderately confident** (0.1-0.5): Hedge with "I think this is likely"
- **Low confidence** (> 0.5): Strong qualifier "This may be unreliable"

### Question Type Sensitivity
- **Mathematical/Factual**: Expected uncertainty 0.0-0.2
- **Technical/Scientific**: Expected uncertainty 0.1-0.4
- **Opinion/Preference**: Expected uncertainty 0.3-0.7
- **Philosophical/Existential**: Expected uncertainty 0.6-1.0

## Design Philosophy

### Why Uncertainty ≠ Emotion
1. **Purpose**: Measurement tool vs. psychological modeling
2. **Function**: Epistemic assessment vs. behavioral modification
3. **Output**: Transparency qualifier vs. emotional expression
4. **Target**: AI safety vs. human-like psychology

### AI Safety Focus
- **Transparency**: Users know when AI is uncertain
- **Reliability**: Qualification prevents overconfidence
- **Calibration**: Uncertainty correlates with actual error rates
- **Trust**: Honest admission of limitations builds appropriate trust

## Research Applications

This demonstrates:
- **Epistemic uncertainty**: Measuring AI knowledge limitations
- **Response calibration**: Aligning confidence with accuracy
- **Transparency mechanisms**: Making AI uncertainty visible to users
- **Safety through honesty**: Preventing dangerous overconfidence
- **Measurable reliability**: Quantifying AI response quality