import json
import pandas as pd
from openai import OpenAI
from pathlib import Path
from tqdm import tqdm

# ------------------
# CONFIG
# ------------------

MODEL = "qwen3:8b"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# ------------------
# LOAD DATA
# ------------------

with open("data/scenarios.json", "r", encoding="utf-8") as f:
    scenarios = json.load(f)

# ------------------
# LOAD PROMPTS
# ------------------

prompt_files = {
    "baseline": "prompts/baseline.txt",
    "role": "prompts/role_prompt.txt",
    "few_shot": "prompts/few_shot.txt"
}

prompts = {}

for name, path in prompt_files.items():
    with open(path, "r", encoding="utf-8") as f:
        prompts[name] = f.read()

# ------------------
# GENERATION
# ------------------

results = []

for strategy, template in prompts.items():

    print(f"\nRunning strategy: {strategy}")

    for scenario in tqdm(scenarios):

        facts_text = "\n".join(
            f"- {fact}" for fact in scenario["facts"]
        )

        prompt = template.format(
            intent=scenario["intent"],
            facts=facts_text,
            tone=scenario["tone"]
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert business communication specialist. "
                    "Generate professional emails without placeholders. "
                    "Only use information provided by the user."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
                ],
            temperature=0.3
        )

        email = response.choices[0].message.content

        results.append({
            "scenario_id": scenario["id"],
            "strategy": strategy,
            "intent": scenario["intent"],
            "tone": scenario["tone"],
            "generated_email": email
        })

# ------------------
# SAVE
# ------------------

df = pd.DataFrame(results)

Path("outputs").mkdir(exist_ok=True)

df.to_csv(
    "outputs/generations.csv",
    index=False
)

print("\nSaved:")
print("outputs/generations.csv")