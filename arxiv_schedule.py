"""Time helpers for the arXiv publication workflow."""

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


UTC = timezone.utc
DISPLAY_TIMEZONE = ZoneInfo("Asia/Shanghai")


def utc_now():
    """Return the current time as an aware UTC datetime."""
    return datetime.now(UTC)


def as_utc(run_at):
    """Normalize an aware datetime to UTC."""
    if run_at.tzinfo is None or run_at.utcoffset() is None:
        raise ValueError("run_at must include timezone information")
    return run_at.astimezone(UTC)


def build_filter_window(lookback_days, run_at=None):
    """Return the UTC interval used to filter arXiv API results."""
    if lookback_days <= 0:
        raise ValueError("lookback_days must be greater than zero")

    end = as_utc(run_at) if run_at is not None else utc_now()
    return end - timedelta(days=lookback_days), end


def format_issue_title(run_at=None):
    """Format an Issue title in the repository owner's local timezone."""
    current = as_utc(run_at) if run_at is not None else utc_now()
    return current.astimezone(DISPLAY_TIMEZONE).strftime("%Y-%m-%d-%H")
