from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowScheduleTests(unittest.TestCase):
    def test_runs_after_arxiv_announcements_on_weekdays_only(self):
        workflow = (ROOT / ".github" / "workflows" / "main.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn('cron: "30 2 * * 1-5"', workflow)
        self.assertNotIn('cron: "10 20 * * 1,2,3,4,5,6"', workflow)


if __name__ == "__main__":
    unittest.main()
