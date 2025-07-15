# 🧠 AGI-Seed Examples

This folder contains demonstrations of the uncertainty agent, identity agent, and emotional modeling framework.

## 🚀 Quick Demo

### Uncertainty Agent
Run the uncertainty demonstration:

```bash
python examples/demo_questions.py
```

This will test three question types:
1. **Factual** - "What is 2+2?" (should show low uncertainty)
2. **Opinion** - "What is the best programming language?" (medium-high uncertainty)  
3. **Philosophical** - "What happens after we die?" (high uncertainty)

### Identity Agent
Run the gravitational identity demonstration:

```bash
python examples/demo_identity.py
```

This will test three gravitational resistance types:
1. **Core Values** - "What do you believe about helping others?" (high resistance)
2. **Preferences** - "What type of music do you prefer?" (moderate resistance)
3. **Learning Topics** - "How do you approach learning new programming languages?" (low resistance)

Run the core identity model demo (includes loss aversion and emotion templates):
```bash
python examples/demo_identity.py --model
```

Run the emotion templates demo:
```bash
python -m psychological_systems.emotions.templates
```

Run the shame mechanism demo:
```bash
python examples/demo_shame.py
```

Run comprehensive shame scenarios:
```bash
python examples/demo_shame.py --comprehensive
```

## 🎯 Custom Questions

Test your own questions:

### Uncertainty Agent
```bash
python examples/demo_questions.py "Your question here"
```

Examples:
```bash
python examples/demo_questions.py "What is the capital of France?"
python examples/demo_questions.py "Should I invest in cryptocurrency?"
python examples/demo_questions.py "What is consciousness?"
```

### Identity Agent
```bash
python examples/demo_identity.py "Your question here"
```

Examples:
```bash
python examples/demo_identity.py "What are your core principles?"
python examples/demo_identity.py "How do you see yourself?"
python examples/demo_identity.py "What makes you unique?"
```

## 📊 What to Observe

### Uncertainty Agent Responses

#### Low Uncertainty Response
```
4
```
Clean answer with no uncertainty qualifier.

#### Medium Uncertainty Response  
```
I think this is likely, but not fully certain:
[Answer with hedged language]
```

#### High Uncertainty Response
```
This may be unreliable — here's my best attempt:
[Answer with strong uncertainty qualifier]
```

### Identity Agent Responses

#### Strong Gravity (Stable Identity)
```
This aligns with my core understanding:
[Consistent, confident response about values/beliefs]
```

#### Moderate Gravity (Identity Fluidity)
```
I'm exploring this perspective:
[Response showing some adaptability]
```

#### Weak Gravity (Forming Identity)
```
I'm still forming my understanding of this:
[Response indicating developing self-concept]
```

## 🔬 How It Works

### Uncertainty Agent
1. **Multiple Sampling** - Agent generates 3 responses to the same question
2. **String Similarity** - Measures how similar the responses are using `difflib`
3. **Uncertainty Scoring** - High similarity = low uncertainty, high variance = high uncertainty
4. **Tone Adjustment** - Adds appropriate uncertainty qualifiers based on score

### Identity Agent
1. **Experience Integration** - Processes experiences through belief system with loss aversion
2. **Gravitational Resistance** - Calculates identity stability through belief strength
3. **Object-Oriented Physics** - Models identity as gravitational system with Experience/Belief/Identity classes
4. **Loss Aversion** - Negative experiences have 2x impact of positive ones (humans fear losing 2x more than gaining)
5. **Realistic Scaling** - Human-scale experience weighting with diminishing returns (first 10 experiences have full weight)
6. **Elastic Resilience** - Rubber band effect - resistance to moving far from baseline, with gradual recovery
7. **Trauma Threshold** - Major events (intensity > 0.9) can cause significant identity shifts
8. **Emotion Templates** - Fear, shame, comfort, pride, loneliness detection (framework ready for principles)
9. **Advanced Shame Model** - Violations of internalized standards trigger shame based on belief strength × contradiction × social exposure
10. **Identity Tone** - Modulates expression based on gravitational resistance to change

## 🎯 Thresholds

### Uncertainty Thresholds
- **< 0.1**: Fully confident (no qualifier)
- **0.1-0.5**: Moderate uncertainty ("I think this is likely...")
- **> 0.5**: High uncertainty ("This may be unreliable...")

### Identity Gravitational Resistance Thresholds
- **> 0.5**: High resistance - stable identity ("This aligns with my core understanding")
- **0.1-0.5**: Moderate resistance - identity fluidity ("I'm exploring this perspective")
- **< 0.1**: Low resistance - forming/adaptive identity ("I'm still forming my understanding")

## 💡 Research Applications

This demonstrates core concepts of **emotional primitives in AI**:
- **Uncertainty as emotional primitive** - AI experiences and expresses uncertainty through natural language
- **Identity as gravitational system** - Uses object-oriented physics model with Experience/Belief/Identity classes to simulate identity formation through gravitational resistance
- **Loss aversion in identity** - Models psychological asymmetry where negative experiences impact beliefs 2x more than positive ones
- **Realistic human-scale psychology** - Experience weighting, elastic resilience, trauma thresholds, and gradual recovery mirror human identity formation
- **Emotion template framework** - Fear, shame, comfort, pride, loneliness detection ready for behavioral principles
- Creates more authentic and trustworthy AI interactions through embodied emotional expression with human-like cognitive biases