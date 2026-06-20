# AI Email Assistant

## Overview

This project implements an AI-powered email generation assistant that creates professional business emails from three inputs:

* Intent
* Key Facts
* Tone

Three prompting strategies were evaluated:

1. Baseline (Zero-Shot)
2. Role-Based Prompting
3. Few-Shot Prompting

The project uses Qwen3:8B running locally through Ollama via the OpenAI-compatible API.

---

## Project Structure

```text
data/
├── scenarios.json

outputs/
├── generations.csv
├── evaluation_llm.csv
├── evaluation_rule_based.csv
├── summary_comparison.csv
├── summary_llm.csv
└── summary_rule_based.csv

prompts/
├── baseline.txt
├── role_prompt.txt
├── few_shot.txt
├── judge_ifs.txt
├── judge_tcs.txt
└── judge_pce.txt

src/
├── generate.py
├── evaluate_llm.py
├── evaluate_rule_based.py
├── metrics.py
└── summary.py
```

---

## Dataset

The file `data/scenarios.json` is the central dataset used throughout the project.

Each scenario contains:

* Scenario ID
* Intent
* Required Facts
* Desired Tone
* Human Reference Email

The dataset is used in two stages:

### Generation

`generate.py` loads each scenario and inserts the intent, facts, and tone into the selected prompt template.

Output:

```text
outputs/generations.csv
```

### Evaluation

`evaluate_llm.py` loads the same scenarios and uses the facts and tone as evaluation criteria for the LLM judge.

Output:

```text
outputs/evaluation_llm.csv
```

---

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Ollama

```bash
ollama serve
```

### Download the Model

```bash
ollama pull qwen3:8b
```

Verify installation:

```bash
ollama list
```

Expected output should include:

```text
qwen3:8b
```

---

## Running the Project

### Step 1: Generate Emails

```bash
python src/generate.py
```

Output:

```text
outputs/generations.csv
```

---

### Step 2: Run Evaluations

LLM-as-a-Judge evaluation:

```bash
python src/evaluate_llm.py
```

Output:

```text
outputs/evaluation_llm.csv
```

Rule-based evaluation:

```bash
python src/evaluate_rule_based.py
```

Output:

```text
outputs/evaluation_rule_based.csv
```

---

### Step 3: Generate Summary Tables

```bash
python src/summary.py
```

Outputs:

```text
outputs/summary_llm.csv
outputs/summary_rule_based.csv
outputs/summary_comparison.csv
```

---

## Evaluation Metrics

### Information Fidelity Score (IFS)

Measures how accurately the generated email preserves the required facts.

### Tone Consistency Score (TCS)

Measures how well the generated email matches the requested tone.

### Professional Communication Effectiveness (PCE)

Measures overall professionalism, clarity, readability, and business appropriateness.

### Placeholder Penalty Score (PPS)

Detects unresolved placeholders such as:

```text
[Customer Name]
[Company Name]
<email>
{contact_name}
```

---

## Included Results

The repository already contains generated outputs and evaluation results.

Key files:

```text
outputs/generations.csv
outputs/evaluation_llm.csv
outputs/evaluation_rule_based.csv
outputs/summary_comparison.csv
```

These files can be inspected directly without rerunning the pipeline.
