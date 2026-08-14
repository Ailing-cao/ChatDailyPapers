import os
import unittest
from unittest.mock import Mock, patch

import github_issue


class MakeGitHubIssueTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "GITHUB_TOKEN": "test-token",
            "GITHUB_REPOSITORY": "owner/repository",
        },
        clear=True,
    )
    @patch("github_issue.requests.post")
    def test_creates_issue_with_standard_endpoint(self, post):
        response = Mock()
        response.json.return_value = {
            "number": 42,
            "html_url": "https://github.com/owner/repository/issues/42",
        }
        post.return_value = response

        issue = github_issue.make_github_issue(
            "Daily papers", body="content", labels=["robotics"]
        )

        self.assertEqual(issue["number"], 42)
        post.assert_called_once_with(
            "https://api.github.com/repos/owner/repository/issues",
            json={"title": "Daily papers", "body": "content", "labels": ["robotics"]},
            headers={
                "Authorization": "Bearer test-token",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30,
        )

    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repository"}, clear=True)
    def test_requires_github_token(self):
        with self.assertRaisesRegex(RuntimeError, "GITHUB_TOKEN"):
            github_issue.make_github_issue("Daily papers")

    @patch.dict(
        os.environ,
        {
            "GITHUB_TOKEN": "test-token",
            "GITHUB_REPOSITORY": "owner/repository",
        },
        clear=True,
    )
    @patch("github_issue.requests.post")
    def test_api_failure_is_not_silenced(self, post):
        response = Mock()
        response.text = '{"message":"Bad credentials"}'
        response.raise_for_status.side_effect = github_issue.requests.HTTPError("401")
        post.return_value = response

        with self.assertRaises(github_issue.requests.HTTPError):
            github_issue.make_github_issue("Daily papers")


if __name__ == "__main__":
    unittest.main()
