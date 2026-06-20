import pandas as pd


# ==================================================
# LOAD RESULTS
# ==================================================

rule_df = pd.read_csv(
    "outputs/evaluation_rule_based.csv"
)

llm_df = pd.read_csv(
    "outputs/evaluation_llm.csv"
)


# ==================================================
# RULE-BASED SUMMARY
# ==================================================

rule_summary = (
    rule_df.groupby("strategy")[["IFS", "PCE", "PPS"]]
    .mean()
    .round(3)
)

rule_summary.to_csv(
    "outputs/summary_rule_based.csv"
)


# ==================================================
# LLM SUMMARY
# ==================================================

llm_summary = (
    llm_df.groupby("strategy")[["IFS", "TCS", "PCE", "PPS"]]
    .mean()
    .round(3)
)
llm_summary.to_csv(
    "outputs/summary_llm.csv"
)


# ==================================================
# COMPARISON TABLE
# ==================================================

comparison_rows = []

for strategy in sorted(
    set(rule_summary.index)
    & set(llm_summary.index)
):

    row = {
        "strategy": strategy
    }

    for metric in rule_summary.columns:
        row[f"Rule_{metric}"] = rule_summary.loc[
            strategy,
            metric
        ]

    for metric in llm_summary.columns:
        row[f"LLM_{metric}"] = llm_summary.loc[
            strategy,
            metric
        ]

    comparison_rows.append(row)

comparison = pd.DataFrame(
    comparison_rows
)

comparison = comparison.round(3)

comparison.to_csv(
    "outputs/summary_comparison.csv"
)


# ==================================================
# PRINT RESULTS
# ==================================================

print("\n" + "=" * 60)
print("RULE-BASED EVALUATION SUMMARY")
print("=" * 60)

print(rule_summary)

print("\n" + "=" * 60)
print("LLM-AS-A-JUDGE EVALUATION SUMMARY")
print("=" * 60)

print(llm_summary)

print("\n" + "=" * 60)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 60)

print(comparison)

print("\nSaved Files:")
print(" - outputs/summary_rule_based.csv")
print(" - outputs/summary_llm.csv")
print(" - outputs/summary_comparison.csv")