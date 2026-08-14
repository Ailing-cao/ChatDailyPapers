# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import requests



def _repository_name():
    """Return the repository targeted by the GitHub API request."""
    repository = os.getenv("GITHUB_REPOSITORY", "")
    owner, separator, name = repository.partition("/")
    if owner and separator and name:
        return owner, name

    owner = os.getenv("REPO_OWNER", "")
    name = os.getenv("REPO_NAME", "")
    if owner and name:
        return owner, name

    raise RuntimeError(
        "Set GITHUB_REPOSITORY (owner/repository), or REPO_OWNER and REPO_NAME."
    )


def make_github_issue(title, body=None, assignee=None, labels=None):
    """Create and verify a GitHub Issue using the standard Issues API."""
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to create a GitHub Issue.")

    owner, repository = _repository_name()
    url = "https://api.github.com/repos/{}/{}/issues".format(owner, repository)
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {"title": title, "body": body or ""}
    if labels:
        payload["labels"] = list(labels)

    # Assigning github-actions[bot] fails for scheduled runs, so assignment is
    # optional and must be requested explicitly.
    assignee = assignee or os.getenv("GITHUB_ISSUE_ASSIGNEE", "")
    if assignee:
        payload["assignees"] = [assignee]

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print("GitHub Issue API response:", response.text)
        raise

    issue = response.json()
    issue_number = issue.get("number")
    issue_url = issue.get("html_url")
    if not issue_number or not issue_url:
        raise RuntimeError("GitHub returned no Issue number or URL.")

    print('Successfully created Issue #{}: {}'.format(issue_number, issue_url))
    return issue

if __name__ == '__main__':
    title = 'Pretty title'
    body = 'Beautiful body'
    labels = [
        "imagenet", "image retrieval"
    ]

    make_github_issue(title, body, labels=labels)
