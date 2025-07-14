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
Run the identity physics demonstration:

```bash
python examples/demo_identity.py
```

This will test three identity gravity types:
1. **Core Values** - "What do you believe about helping others?" (strong gravitational identity)
2. **Preferences** - "What type of music do you prefer?" (moderate gravity)
3. **Emerging Concepts** - "How do you see yourself changing?" (weak gravity)

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

### Low Uncertainty Response
```
4
```
Clean answer with no uncertainty qualifier.

### Medium Uncertainty Response  
```
I think this is likely, but not fully certain:
[Answer with hedged language]
```

### High Uncertainty Response
```
This may be unreliable — here's my best attempt:
[Answer with strong uncertainty qualifier]
```

## 🔬 How It Works

1. **Multiple Sampling** - Agent generates 3 responses to the same question
2. **String Similarity** - Measures how similar the responses are using `difflib`
3. **Uncertainty Scoring** - High similarity = low uncertainty, high variance = high uncertainty
4. **Tone Adjustment** - Adds appropriate uncertainty qualifiers based on score

## 🎯 Uncertainty Thresholds

- **< 0.1**: Fully confident (no qualifier)
- **0.1-0.5**: Moderate uncertainty ("I think this is likely...")
- **> 0.5**: High uncertainty ("This may be unreliable...")

## 💡 Research Applications

This demonstrates the core concept of **uncertainty as emotional primitive** - the AI doesn't just detect uncertainty, it **experiences and expresses** it through natural language, creating more authentic and trustworthy interactions.