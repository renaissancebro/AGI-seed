# models/models.py

from openai import OpenAI
import time
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_model(prompt, n_samples=3):
    completions = []
    for _ in range(n_samples):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        completions.append(response.choices[0].message.content)
        time.sleep(1.1)  # prevent rate limit
    return completions
