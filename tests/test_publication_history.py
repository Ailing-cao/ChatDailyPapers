import tempfile
import unittest
from pathlib import Path

from publication_history import load_published_paper_ids, paper_id_from_url


class PublicationHistoryTests(unittest.TestCase):
    def test_extracts_version_independent_arxiv_id(self):
        self.assertEqual(
            paper_id_from_url("http://arxiv.org/abs/2608.17512v2"),
            "2608.17512",
        )
        self.assertEqual(
            paper_id_from_url("https://arxiv.org/pdf/2608.26932v1.pdf"),
            "2608.26932",
        )

    def test_loads_unique_ids_from_existing_exports(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            export_directory = Path(temporary_directory)
            (export_directory / "one.md").write_text(
                "- Url: http://arxiv.org/abs/2608.17512v1\n",
                encoding="utf-8",
            )
            (export_directory / "two.md").write_text(
                "https://arxiv.org/abs/2608.17512v2\n"
                "https://arxiv.org/pdf/2608.26932v1.pdf\n",
                encoding="utf-8",
            )

            self.assertEqual(
                load_published_paper_ids(export_directory),
                {"2608.17512", "2608.26932"},
            )

    def test_missing_export_directory_is_empty(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing = Path(temporary_directory) / "missing"
            self.assertEqual(load_published_paper_ids(missing), set())


if __name__ == "__main__":
    unittest.main()
