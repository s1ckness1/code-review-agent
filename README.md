# Code Review Agent

An automated code review agent powered by Claude (Anthropic) that analyzes pull request diffs and generates structured, actionable inline review comments — reducing review bottlenecks for small engineering teams.

---

## Problem It Solves

On small teams (5–20 devs), developers often wait hours for PR reviews on straightforward changes. This agent automates the first-pass review, catching bugs, security issues, and style violations instantly — so human reviewers can focus on architecture and intent.

---

## Core Logic Flow

```
GitHub Webhook (PR opened/updated)
        │
        ▼
  1. Fetch Git Diff + Codebase Context
        │
        ▼
  2. Claude Agent — Long-chain Reasoning Pass
     ├─ Bug detection
     ├─ Security vulnerability scan
     └─ Style & best practice violations
        │
        ▼
  3. Generate Structured Inline Comments
        │
        ▼
  4. Second Agent Pass — False Positive Filter (closed-loop verification)
        │
        ▼
  5. Post Comments to GitHub PR via API
```

---

## Features

- Multi-step agentic reasoning with Claude API
- Closed-loop verification to reduce false positives
- GitHub webhook integration
- Supports Python, JavaScript, TypeScript
- Structured JSON output for inline PR comments

---

## Tech Stack

- **LLM**: Claude claude-sonnet-4-20250514 (Anthropic)
- **Language**: Python 3.11+
- **Integrations**: GitHub REST API, Webhooks
- **Framework**: FastAPI (webhook server)

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/code-review-agent
cd code-review-agent
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY and GITHUB_TOKEN to .env
```

---

## 🔧 Usage

```bash
# Start the webhook server
python src/server.py

# Or run manually on a diff file
python src/agent.py --diff path/to/diff.patch
```

---

## Project Structure

```
code-review-agent/
├── src/
│   ├── agent.py          # Core multi-agent logic
│   ├── github_client.py  # GitHub API integration
│   ├── server.py         # FastAPI webhook server
│   └── prompts.py        # Claude prompt templates
├── tests/
│   └── test_agent.py
├── docs/
│   └── architecture.md
├── .env.example
├── requirements.txt
└── README.md
```

---

## Estimated Usage

| Metric | Value |
|--------|-------|
| Avg tokens/review | ~8,000 |
| PRs/day (target) | 50–100 |
| Estimated tokens/day | 400K–800K |

---

## License

MIT
