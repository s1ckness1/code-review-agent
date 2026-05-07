"""
agent.py — Core multi-agent review logic using Claude API
"""

import os
import json
import argparse
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

REVIEW_SYSTEM_PROMPT = """You are an expert code reviewer. Analyze the provided Git diff and return a JSON array of review comments.

Each comment must follow this structure:
{
  "file": "path/to/file.py",
  "line": 42,
  "severity": "error" | "warning" | "suggestion",
  "category": "bug" | "security" | "style" | "performance",
  "comment": "Clear, actionable explanation"
}

Return ONLY valid JSON. No markdown, no preamble."""

FILTER_SYSTEM_PROMPT = """You are a senior engineer reviewing AI-generated code comments for false positives.
Given a list of review comments and the original diff, remove any comments that are:
- Incorrect or based on misreading the code
- Too nitpicky to be useful
- Duplicates

Return the filtered list as valid JSON only."""


def fetch_diff(diff_path: str) -> str:
    with open(diff_path, "r") as f:
        return f.read()


def run_review_agent(diff: str) -> list:
    """Pass 1: Generate review comments via long-chain reasoning."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=REVIEW_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Review this diff:\n\n```diff\n{diff}\n```"
            }
        ]
    )
    raw = response.content[0].text
    return json.loads(raw)


def run_filter_agent(diff: str, comments: list) -> list:
    """Pass 2: Closed-loop false positive filter."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=FILTER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Original diff:\n```diff\n{diff}\n```\n\n"
                    f"Review comments to filter:\n{json.dumps(comments, indent=2)}"
                )
            }
        ]
    )
    raw = response.content[0].text
    return json.loads(raw)


def review(diff_path: str) -> list:
    """Full agentic pipeline: review → filter → return."""
    diff = fetch_diff(diff_path)
    print(f"[1/2] Running review agent on {diff_path}...")
    comments = run_review_agent(diff)
    print(f"      → {len(comments)} comments generated")

    print("[2/2] Running filter agent (closed-loop verification)...")
    filtered = run_filter_agent(diff, comments)
    print(f"      → {len(filtered)} comments after filtering")

    return filtered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Review Agent")
    parser.add_argument("--diff", required=True, help="Path to .patch / diff file")
    args = parser.parse_args()

    results = review(args.diff)
    print("\n=== Review Results ===")
    print(json.dumps(results, indent=2))
