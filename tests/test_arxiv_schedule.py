import unittest
from datetime import datetime, timedelta, timezone

from arxiv_schedule import build_filter_window, format_issue_title


class ArxivScheduleTests(unittest.TestCase):
    def test_filter_window_uses_aware_utc_times(self):
        run_at = datetime(2026, 8, 28, 2, 30, tzinfo=timezone.utc)

        start, end = build_filter_window(4.0, run_at=run_at)

        self.assertEqual(end, run_at)
        self.assertEqual(start, run_at - timedelta(days=4.0))
        self.assertEqual(start.utcoffset(), timedelta(0))

    def test_issue_title_uses_asia_shanghai_time(self):
        run_at = datetime(2026, 8, 28, 2, 30, tzinfo=timezone.utc)

        self.assertEqual(format_issue_title(run_at), "2026-08-28-10")

    def test_naive_run_time_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            build_filter_window(4.0, run_at=datetime(2026, 8, 28, 2, 30))

    def test_non_positive_lookback_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            build_filter_window(0)


if __name__ == "__main__":
    unittest.main()
