import unittest
from textwrap import dedent

from update_readme import ArgumentParser as UpdateReadmeArgs
from update_readme import update_readme


class TestUpdateReadme(unittest.TestCase):
    def setup_update_readme_args(self, manifest: str, readme: str):
        return UpdateReadmeArgs().from_dict(
            {
                "readme": readme,
                "readme_path": None,
                "manifest": dedent(manifest).strip(),
                "manifest_url": None,
            }
        )

    def test_does_nothing_if_current(self):
        manifest = """
        name
        admin_boundaries_2024-01-01.versatiles
        admin_boundaries_2025-01-01.versatiles
        admin_labels_2024-01-01.versatiles
        admin_labels_2025-01-01.versatiles
        """

        readme = dedent("""
        <!-- BEGIN TIMESTAMPS -->
        `2024-01-01`, `2025-01-01`
        <!-- END TIMESTAMPS -->
        """).strip()

        self.assertEqual(
            update_readme(
                self.setup_update_readme_args(
                    manifest,
                    readme,
                )
            ),
            readme,
        )

    def test_adds_missing_timestamp(self):
        manifest = """
        name
        admin_labels_2024-01-01.versatiles
        admin_labels_2025-01-01.versatiles
        admin_labels_2026-01-01.versatiles
        """

        readme = dedent("""
        <!-- BEGIN TIMESTAMPS -->
        `2024-01-01`, `2025-01-01`
        <!-- END TIMESTAMPS -->
        """).strip()

        self.assertEqual(
            update_readme(
                self.setup_update_readme_args(
                    manifest,
                    readme,
                )
            ),
            dedent("""
            <!-- BEGIN TIMESTAMPS -->
            `2024-01-01`, `2025-01-01`, `2026-01-01`
            <!-- END TIMESTAMPS -->
            """).strip(),
        )

    def test_removes_extra_timestamp(self):
        manifest = """
        name
        admin_labels_2024-01-01.versatiles
        admin_labels_2025-01-01.versatiles
        """

        readme = dedent("""
        <!-- BEGIN TIMESTAMPS -->
        `2024-01-01`, `2025-01-01`, `2026-01-01`
        <!-- END TIMESTAMPS -->
        """).strip()

        self.assertEqual(
            update_readme(
                self.setup_update_readme_args(
                    manifest,
                    readme,
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
