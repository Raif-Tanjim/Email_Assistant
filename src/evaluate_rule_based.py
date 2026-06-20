import json
import pandas as pd

from metrics import placeholder_penalty_score


# ==================================================
# RULE-BASED IFS
# ==================================================

def information_fidelity_score(facts, email_text):
    """
    Simple fact coverage metric.

    Score = facts detected / total facts
    """

    email_lower = email_text.lower()

    matched = 0

    for fact in facts:

        fact_words = [
            w.lower()
            for w in fact.split()
            if len(w) > 3
        ]

        hits = sum(
            1
            for word in fact_words
            if word in email_lower
        )

        if len(fact_words) == 0:
            continue

        coverage = hits / len(fact_words)

        if coverage >= 0.5:
            matched += 1

    return round(
        matched / len(facts),
        3
    )


# ==================================================
# RULE-BASED PCE
# ==================================================

def professional_communication_effectiveness(email_text):

    score = 0

    text = email_text.lower()

    # Subject
    if "subject:" in text:
        score += 1

    # Greeting
    if any(
        g in text
        for g in ["dear", "hello", "hi"]
    ):
        score += 1

    # Closing
    if any(
        c in text
        for c in [
            "best regards",
            "kind regards",
            "sincerely",
            "warm regards"
        ]
    ):
        score += 1

    # Length
    words = len(
        email_text.split()
    )

    if 80 <= words <= 250:
        score += 1

    # Paragraph structure
    if email_text.count("\n\n") >= 3:
        score += 1

    return round(
        score / 5,
        3
    )
# ==================================================
# LOAD DATA
# ==================================================

with open(
    "data/scenarios.json",
    "r",
    encoding="utf-8"
) as f:

    scenarios = json.load(f)

scenario_lookup = {
    s["id"]: s
    for s in scenarios
}


# ==================================================
# LOAD GENERATIONS
# ==================================================

df = pd.read_csv(
    "outputs/generations.csv"
)

results = []


# ==================================================
# EVALUATION
# ==================================================

for _, row in df.iterrows():

    scenario_id = int(
        row["scenario_id"]
    )

    scenario = scenario_lookup[
        scenario_id
    ]

    email_text = row[
        "generated_email"
    ]

    facts = scenario[
        "facts"
    ]

    ifs = information_fidelity_score(
        facts,
        email_text
    )

    pce = professional_communication_effectiveness(
        email_text
    )

    pps = placeholder_penalty_score(
        email_text
    )

    results.append({
        "scenario_id":
            scenario_id,

        "strategy":
            row["strategy"],

        "IFS":
            ifs,

        "PCE":
            pce,

        "PPS":
            pps
    })


# ==================================================
# SAVE
# ==================================================

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "outputs/evaluation_rule_based.csv",
    index=False
)

print(
    "\nSaved:"
)

print(
    "outputs/evaluation_rule_based.csv"
)

print()
print(
    results_df.head()
)