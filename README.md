# Job Application Screener — Claude vs OpenAI Comparison Tool

Compares Anthropic's Claude and OpenAI's GPT-4o-mini on the same resume-screening prompt, side by side — response quality, token cost per call, and latency.

## What it compares

- **Response text** — how each model rates a candidate's fit against a job description
- **Cost per call** — real input/output token cost in dollars, calculated from each API's actual token usage
- **Latency** — wall-clock time for each API call

## Setup

1. Clone the repo and create a virtual environment:
```bash
   git clone https://github.com/aviraljoshi27/job-application-screener.git
   cd job-application-screener
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
   pip install anthropic openai python-dotenv
```

3. Create a `.env` file in the project root with your API keys:
```
   ANTHROPIC_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
```
   Both variable names must match exactly — the code reads them via `os.getenv()`.

## Usage

```bash
python compare.py
```

This sends the same job description + resume prompt to both Claude (`claude-sonnet-4-6`) and GPT-4o-mini, then prints each model's response, token usage, latency, and cost side by side.

## Example output

```
========================================
📝 PROMPT VISUAL COMPARISON
========================================
-------------Claude Output--------------
Text: ## Candidate Fit Rating: **6.5/10**
---
**Justification:**
Alex demonstrates strong alignment with the core technical stack — React, Next.js, and TypeScript in production — which directly addresses the role's primary requirements, and the CI/CD experience signals solid engineering maturity. However, the **1-year experience gap** (4 vs. 5+ years required) and the **complete absence of AWS/cloud experience** leave two
Input Tokens Used: 135
Output Tokens Used: 100
Latency: 4.185798
--------------Claude Price--------------
Input Price : $0.000405,
Output Price : $0.001500
---------------GPT Output---------------
Text: Rating: 5/10
Justification: While Alex has strong experience with React, Next.js, and TypeScript, they fall short in the required experience, having only 4 years instead of the 5+ necessary. Additionally, the lack of cloud or AWS experience may limit their effectiveness in a role that could potentially involve serverless architecture or cloud deployments.
Input Tokens Used: 116
Output Tokens Used: 73
Latency: 3.165801
---------------GPT Price----------------
Input Price : $0.000017,
Output Price : $0.000044
```

## Error handling

Each API call is wrapped independently and fails soft — if one provider's call fails (rate limit, bad key, invalid model name, connection issue), the tool still prints the other provider's full result instead of crashing the whole comparison.

## Scope

This is a learning-phase project built while working through the fundamentals of both SDKs — not a final portfolio deliverable. It's a teaching example for comparing raw API usage, cost, and latency across two providers.