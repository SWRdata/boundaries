import unittest
from textwrap import dedent

from scripts.update_readme import ArgumentParser, update_readme


class TestUpdateReadme(unittest.TestCase):
    def make_args(self, manifest: str, readme: str):
        return ArgumentParser().from_dict(
            {
                "readme": dedent(readme).strip(),
                "readme_path": None,
                "manifest": dedent(manifest).strip(),
                "manifest_url": None,
                "quiet": True,
            }
        )

    def test_does_nothing_if_current(self):

        self.assertEqual(
            update_readme(
                self.make_args(
                    """
                    name
                    admin_boundaries_2024-01-01.versatiles
                    admin_boundaries_2025-01-01.versatiles
                    admin_labels_2024-01-01.versatiles
                    admin_labels_2025-01-01.versatiles
                    """,
                    """
                    <!-- BEGIN TIMESTAMPS -->
                    `2024-01-01`, `2025-01-01`
                    <!-- END TIMESTAMPS -->
                    """,
                )
            ),
            dedent("""
            <!-- BEGIN TIMESTAMPS -->
            `2024-01-01`, `2025-01-01`
            <!-- END TIMESTAMPS -->
            """).strip(),
        )

    def test_adds_missing_timestamp(self):

        self.assertEqual(
            update_readme(
                self.make_args(
                    """
                    name
                    admin_labels_2024-01-01.versatiles
                    admin_labels_2025-01-01.versatiles
                    admin_labels_2026-01-01.versatiles
                    """,
                    """
                    <!-- BEGIN TIMESTAMPS -->
                    `2024-01-01`, `2025-01-01`
                    <!-- END TIMESTAMPS -->
                    """,
                )
            ),
            dedent("""
            <!-- BEGIN TIMESTAMPS -->
            `2024-01-01`, `2025-01-01`, `2026-01-01`
            <!-- END TIMESTAMPS -->
            """).strip(),
        )

    def test_removes_extra_timestamp(self):

        self.assertEqual(
            update_readme(
                self.make_args(
                    """
                    name
                    admin_labels_2024-01-01.versatiles
                    admin_labels_2025-01-01.versatiles
                    """,
                    """
                    <!-- BEGIN TIMESTAMPS -->
                    `2024-01-01`, `2025-01-01`, `2026-01-01`
                    <!-- END TIMESTAMPS -->
                    """,
                )
            ),
            dedent("""
            <!-- BEGIN TIMESTAMPS -->
            `2024-01-01`, `2025-01-01`
            <!-- END TIMESTAMPS -->
            """).strip(),
        )


if __name__ == "__main__":
    unittest.main()
