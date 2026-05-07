"""
server.py — FastAPI webhook server for GitHub PR events
"""

import hmac
import hashlib
import os
from fastapi import FastAPI, Request, HTTPException
from src.agent import review
from src.github_client import get_pr_diff, post_review_comments

app = FastAPI(title="Code Review Agent")
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")

    if WEBHOOK_SECRET and not verify_signature(payload, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()
    if data.get("action") not in ("opened", "synchronize"):
        return {"status": "skipped"}

    pr = data["pull_request"]
    owner, repo = data["repository"]["full_name"].split("/")
    pr_number = pr["number"]
    commit_sha = pr["head"]["sha"]

    # Fetch diff from GitHub
    diff_text = get_pr_diff(owner, repo, pr_number)

    # Write to temp file for agent
    tmp_path = f"/tmp/pr_{pr_number}.patch"
    with open(tmp_path, "w") as f:
        f.write(diff_text)

    # Run agent pipeline
    comments = review(tmp_path)

    # Post back to GitHub
    if comments:
        post_review_comments(owner, repo, pr_number, commit_sha, comments)

    return {"status": "ok", "comments_posted": len(comments)}


@app.get("/health")
def health():
    return {"status": "healthy"}
