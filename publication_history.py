"""Track arXiv papers that have already been published by this workflow."""

import re
from pathlib import Path


ARXIV_ID_PATTERN = re.compile(
    r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/([^\s/#?]+?)(?:v\d+)?(?:\.pdf)?(?:[\s/#?]|$)",
    re.IGNORECASE,
)


def paper_id_from_url(url):
    """Return a version-independent arXiv identifier from a URL."""
    match = ARXIV_ID_PATTERN.search(url or "")
    return match.group(1) if match else None


def load_published_paper_ids(export_path="export"):
    """Read arXiv identifiers from previously committed Markdown exports."""
    published_ids = set()
    export_directory = Path(export_path)
    if not export_directory.exists():
        return published_ids

    for markdown_file in export_directory.glob("*.md"):
        text = markdown_file.read_text(encoding="utf-8", errors="ignore")
        for match in ARXIV_ID_PATTERN.finditer(text):
            published_ids.add(match.group(1))
    return published_ids
