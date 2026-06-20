import json
import re
import pandas as pd
from pathlib import Path

from openai import OpenAI
from metrics import placeholder_penalty_score


# ==================================================
# CONFIG
# ==================================================

MODEL = "qwen3:8b"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# ==================================================
# LOAD JUDGE PROMPTS
# ==================================================

with open("prompts/judge_ifs.txt", "r", encoding="utf-8") as f:
    IFS_TEMPLATE = f.read()

with open("prompts/judge_tcs.txt", "r", encoding="utf-8") as f:
    TCS_TEMPLATE = f.read()

with open("prompts/judge_pce.txt", "r", encoding="utf-8") as f:
    PCE_TEMPLATE = f.read()


# ==================================================
# LOAD DATA
# ==================================================

with open("data/scenarios.json", "r", encoding="utf-8") as f:
    scenarios = json.load(f)

scenario_lookup = {
    s["id"]: s
    for s in scenarios
}

generations = pd.read_csv(
    "outputs/generations.csv"
)


# ==================================================
# HELPER
# ==================================================

def extract_score(response_text):

    match = re.search(r"[1-5]", response_text)

    if match:
        return int(match.group())

    return None


def judge(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an objective evaluator. "
                    "Return only a single score."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# ==================================================
# EVALUATION
# ==================================================

results = []

total = len(generations)

for idx, row in generations.iterrows():

    scenario_id = int(row["scenario_id"])

    scenario = scenario_lookup[
        scenario_id
    ]

    facts_text = "\n".join(
        f"- {fact}"
        for fact in scenario["facts"]
    )

    email = row["generated_email"]

    # --------------------------
    # IFS
    # --------------------------

    ifs_prompt = IFS_TEMPLATE.format(
        facts=facts_text,
        email=email
    )

    ifs_raw = judge(ifs_prompt)

    ifs = extract_score(
        ifs_raw
    )

    # --------------------------
    # TCS
    # --------------------------

    tcs_prompt = TCS_TEMPLATE.format(
        tone=scenario["tone"],
        email=email
    )

    tcs_raw = judge(
        tcs_prompt
    )

    tcs = extract_score(
        tcs_raw
    )

    # --------------------------
    # PCE
    # --------------------------

    pce_prompt = PCE_TEMPLATE.format(
        email=email
    )

    pce_raw = judge(
        pce_prompt
    )

    pce = extract_score(
        pce_raw
    )

    # --------------------------
    # PPS
    # --------------------------

    pps = placeholder_penalty_score(
        email
    )

    results.append({

        "scenario_id":
            scenario_id,

        "strategy":
            row["strategy"],

        "IFS":
            ifs,

        "TCS":
            tcs,

        "PCE":
            pce,

        "PPS":
            pps

    })

    print(
        f"[{idx+1}/{total}] "
        f"{row['strategy']} "
        f"Scenario {scenario_id}"
    )


# ==================================================
# SAVE
# ==================================================

results_df = pd.DataFrame(
    results
)

Path("outputs").mkdir(
    exist_ok=True
)

results_df.to_csv(
    "outputs/evaluation_llm.csv",
    index=False
)

print()
print(
    "Saved:"
)
print(
    "outputs/evaluation_llm.csv"
)