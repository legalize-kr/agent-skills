"""Guard the documented 0.4.0 law-date contract for agent consumers."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class TemporalSemanticsDocsTest(unittest.TestCase):
    def test_skill_explains_both_date_semantics_and_file_scope(self) -> None:
        skill = read("skills/legalize-kr/SKILL.md")
        for expected in (
            "--semantic 공포일자",
            "--semantic 시행일자",
            "file_effective_date_only: true",
            "article-specific commencement dates",
            "before 1970",
            "resolved_version_date",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, skill)

    def test_mcp_reference_preserves_semantic_contract(self) -> None:
        reference = read("skills/legalize-kr/references/access-options.md")
        for expected in (
            "laws_get",
            "laws_article",
            "`semantic` argument",
            "file_effective_date_only",
            "--semantic 시행일자",
            "before 1970",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, reference)

    def test_readme_guides_effective_date_requests(self) -> None:
        readme = read("README.md")
        self.assertIn("시행일자", readme)
        self.assertIn("file_effective_date_only", readme)
        self.assertIn("1970년 이전", readme)


if __name__ == "__main__":
    unittest.main()
