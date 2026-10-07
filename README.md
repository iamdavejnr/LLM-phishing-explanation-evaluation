# Evaluating the Fidelity and Completeness of Multi-Style LLM-Generated Explanations for AI-Based Phishing Detection

**MSc Cybersecurity Technology (Distinction) · Northumbria University · 2026**
Supervisor: Dr Usman Butt

![Python](https://img.shields.io/badge/Python-3.x-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-Random%20Forest-orange) ![SHAP](https://img.shields.io/badge/XAI-SHAP-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview

AI-based phishing detectors can classify emails with very high accuracy, yet the *reasoning* behind each decision is rarely communicated in a form that end users can understand. This project investigates whether Large Language Models (LLMs) can bridge that gap, and which style of explanation does it best.

I built an end-to-end, reproducible pipeline that:

1. Trains a Random Forest phishing classifier
2. Extracts the model's reasoning using SHAP values
3. Uses an LLM (Claude API) to turn that reasoning into three explanation styles: **technical**, **simple** and **narrative**
4. Evaluates all 900 generated explanations with a multi-metric automated framework and tests for statistical significance

## Research Questions

| # | Question |
|---|----------|
| RQ1 | How do technical, simple and narrative explanations differ in **fidelity** to the classifier's underlying reasoning? |
| RQ2 | How do the three styles perform under **LLM-as-Judge** evaluation (accuracy, clarity, completeness)? |
| RQ3 | Which style is **most effective overall** at communicating phishing-detection reasoning? |

## Methodology

```
Kaggle phishing   →  Preprocessing   →  Random Forest   →  SHAP feature   →  LLM explanation   →  Automated      →  Statistical
email dataset        & balancing        classifier         attribution        generation (x3)      evaluation        testing
                                        (+ BERT baseline)  (top-3 features)  300 emails = 900     (5 metrics)       (Kruskal-Wallis)
```

- **Classifier:** Random Forest, selected over a fine-tuned BERT baseline, with recall weighted most heavily because missed phishing emails carry the greatest real-world risk.
- **Reasoning extraction:** SHAP values; the three highest-contribution features per email serve as the ground truth for fidelity.
- **Evaluation sample:** 300 emails, stratified across easy, borderline and complex cases.
- **Explanation styles:** fixed prompt templates applied identically across all emails.
- **Evaluation metrics:**

| Metric | Method |
|--------|--------|
| Fidelity | Proportion of SHAP-identified features referenced in the explanation |
| Readability | Flesch Reading Ease (`textstat`) |
| Accuracy, Clarity, Completeness | Structured LLM-as-Judge rubric |

- **Statistics:** Kruskal-Wallis tests (p < 0.05) per metric.

## Key Results

### Classifier performance

| Accuracy | Precision | Recall | F1 |
|:--:|:--:|:--:|:--:|
| 99.48% | 99.51% | 99.45% | 99.48% |

### Explanation quality by style

| Metric | Technical | Simple | Narrative |
|--------|:--:|:--:|:--:|
| Fidelity (0–1) | **0.788** | 0.192 | 0.152 |
| Readability | -25.14 | 20.25 | **28.91** |
| Accuracy (1–5) | 2.94 | **4.38** | 3.17 |
| Clarity (1–5) | 3.58 | **4.82** | 4.39 |
| Completeness (1–5) | 2.93 | **4.34** | 3.05 |

All five metrics differed significantly between styles (Kruskal-Wallis, p < 0.05; H ranged from 176.9 for accuracy to 633.8 for readability).

### Takeaways

- **There is a measurable fidelity–accessibility trade-off.** Technical explanations mirror the model's reasoning most closely but are the hardest to read and were rated least clear.
- **Simple, plain-language explanations were the most effective overall**, scoring highest on accuracy, clarity and completeness while remaining readable.
- **Narrative explanations were the most readable** but tended to omit indicators or lose precision.
- **Recommendation:** default to plain-language explanations for general users, and offer an adaptive option that exposes technical detail for analysts and auditors.

## Limitations

Being explicit about these is part of the contribution:

- **Single dataset.** Findings may not generalise to newer or more sophisticated phishing campaigns.
- **Judge/generator overlap.** The same model family generated and judged explanations, which risks circularity. Future work should use an independent judge model.
- **Keyword-based fidelity.** Fidelity relies on lexical matching, so it may under-credit explanations that convey a feature using different wording. A semantic similarity measure would be a stronger alternative.
- **No human evaluation.** Automated scores may not reflect real user comprehension or trust.

## Future Work

- Independent LLM judge and semantic fidelity metrics
- Small-scale user study to validate automated findings
- Adaptive explanation systems that tailor style to user expertise
- Extension to other security domains (malware classification, intrusion detection)

## Repository Structure

> *Update this section to match your actual repository.*

```
├── data/                 # Instructions for obtaining the dataset (not redistributed)
├── notebooks/            # Exploration, training and evaluation notebooks
├── src/                  # Preprocessing, classifier, SHAP extraction, generation, evaluation
├── prompts/              # The three prompt templates (technical, simple, narrative)
├── results/              # Evaluation scores, statistical test outputs, figures
├── docs/                 # Dissertation (PDF)
├── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Set your Anthropic API key as an environment variable (never commit it):

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Then run the pipeline in order: preprocessing → classifier training → SHAP extraction → explanation generation → evaluation → statistical analysis.

## Dataset

A publicly available phishing email dataset from Kaggle was used. It is not redistributed here; please see the original source for access and licence terms: `<link to dataset>`.

## Tech Stack

Python · Pandas · NumPy · scikit-learn · SHAP · Hugging Face Transformers (BERT baseline) · Anthropic Claude API · textstat · SciPy · Matplotlib · Seaborn

## Citation

If you build on this work, please cite:

```
Okoroh, D. J. (2026) Evaluating the Fidelity and Completeness of Multi-Style
LLM-Generated Explanations for AI-Based Phishing Detection. MSc dissertation,
Northumbria University.
```

## Author

**David Junior Okoroh**
MSc Cybersecurity Technology, Northumbria University
[LinkedIn](https://www.linkedin.com/in/your-profile) · [Email](mailto:your-email)

## Licence

Code is released under the MIT Licence. The dissertation text is © David Junior Okoroh, all rights reserved.
