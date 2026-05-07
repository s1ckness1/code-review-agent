"""
test_agent.py — Basic tests for the review agent
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from src.agent import run_review_agent, run_filter_agent

SAMPLE_DIFF = """
diff --git a/app.py b/app.py
index 1234567..abcdefg 100644
--- a/app.py
+++ b/app.py
@@ -10,6 +10,10 @@ def get_user(user_id):
+    query = f"SELECT * FROM users WHERE id = {user_id}"
+    result = db.execute(query)
+    password = result["password"]
+    return jsonify(result)
"""

MOCK_COMMENTS = [
    {
        "file": "app.py",
        "line": 13,
        "severity": "error",
        "category": "security",
        "comment": "SQL injection vulnerability: use parameterized queries instead."
    }
]


@patch("src.agent.client")
def test_review_agent_returns_list(mock_client):
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(MOCK_COMMENTS))]
    mock_client.messages.create.return_value = mock_response

    result = run_review_agent(SAMPLE_DIFF)
    assert isinstance(result, list)
    assert result[0]["category"] == "security"


@patch("src.agent.client")
def test_filter_agent_returns_list(mock_client):
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(MOCK_COMMENTS))]
    mock_client.messages.create.return_value = mock_response

    result = run_filter_agent(SAMPLE_DIFF, MOCK_COMMENTS)
    assert isinstance(result, list)
