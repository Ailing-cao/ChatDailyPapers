GITHUB_ISSUE_BODY_LIMIT = 60000


def split_issue_bodies(parts, max_chars=GITHUB_ISSUE_BODY_LIMIT):
    """Pack paper sections into GitHub-safe Issue bodies."""
    blocks = []
    topic = ""
    paper = []

    def flush_paper():
        nonlocal paper
        if paper:
            block = ([topic] if topic else []) + paper
            blocks.append("\n".join(block))
            paper = []

    for part in parts:
        if part.startswith("# "):
            flush_paper()
            topic = part
        elif part.startswith("## "):
            flush_paper()
            paper = [part]
        else:
            paper.append(part)
    flush_paper()

    if not blocks:
        blocks = ["\n".join(parts)] if parts else []

    chunks = []
    current = ""
    for block in blocks:
        candidate = f"{current}\n\n{block}" if current else block
        if current and len(candidate) > max_chars:
            chunks.append(current)
            current = block
        else:
            current = candidate
    if current:
        chunks.append(current)

    safe_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            safe_chunks.append(chunk)
        else:
            safe_chunks.extend(
                chunk[offset : offset + max_chars]
                for offset in range(0, len(chunk), max_chars)
            )
    return safe_chunks
