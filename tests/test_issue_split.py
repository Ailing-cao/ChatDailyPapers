import unittest

from issue_utils import split_issue_bodies


class IssueSplitTests(unittest.TestCase):
    def test_splits_at_paper_boundaries_and_repeats_topic(self):
        parts = [
            "# visual navigation",
            "## First paper",
            "A" * 35,
            "## Second paper",
            "B" * 35,
        ]

        chunks = split_issue_bodies(parts, max_chars=100)

        self.assertEqual(len(chunks), 2)
        self.assertTrue(all(len(chunk) <= 100 for chunk in chunks))
        self.assertTrue(all(chunk.startswith("# visual navigation") for chunk in chunks))
        self.assertIn("## First paper", chunks[0])
        self.assertIn("## Second paper", chunks[1])


if __name__ == "__main__":
    unittest.main()
