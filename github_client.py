"""
github_client.py — GitHub REST API integration
"""

import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github.diff"})
    response.raise_for_status()
    return response.text


def post_review_comments(owner: str, repo: str, pr_number: int, commit_sha: str, comments: list):
    """Post inline review comments to a GitHub PR."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    payload = {
        "commit_id": commit_sha,
        "event": "COMMENT",
        "comments": [
            {
                "path": c["file"],
                "line": c["line"],
                "body": f"**[{c['severity'].upper()}] {c['category']}**\n\n{c['comment']}"
            }
            for c in comments
        ]
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()
