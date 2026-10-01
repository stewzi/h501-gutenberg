import ast
from pathlib import Path
import unittest
from unittest.mock import patch

import matplotlib
import pandas as pd

from tt_gutenberg.authors import list_authors, plot_translations
from tt_gutenberg.transform import birth_centuries, count_languages


matplotlib.use("Agg")


class GutenbergTests(unittest.TestCase):
    def setUp(self):
        self.authors = pd.DataFrame({
            "gutenberg_author_id": [1, 2, 3, 4, 5],
            "author": ["A", "B", "C", "D", "E"],
            "alias": [" Alias A ", None, "Alias C", "", "Alias E"],
            "birthdate": [1753, 1800, None, -25, 1799],
        })
        self.metadata = pd.DataFrame({
            "gutenberg_author_id": [1, 1, 2, 3, 4],
            "language": ["en/fr", "en", "de", None, "es"],
        })

    def test_unique_languages_and_missing_values(self):
        result = count_languages(self.authors, self.metadata)
        self.assertEqual(result["translation_count"].tolist(), [2, 1, 0, 1, 0])

    def test_alias_ranking_and_source_order_ties(self):
        with patch("tt_gutenberg.authors.get_data", return_value=(
            self.authors.merge(
                self.metadata, on="gutenberg_author_id", how="left"
            )
        )):
            result = list_authors(by_languages=True, alias=True)
        self.assertEqual(result, ["Alias A", "Alias C", "Alias E"])
        self.assertIsInstance(result, list)

    def test_birth_centuries(self):
        result = birth_centuries(self.authors)
        self.assertEqual(
            result["birth_century"].tolist(), [1700, 1800, -100, 1700]
        )

    def test_plot_uses_authors_without_aliases(self):
        with patch("tt_gutenberg.authors.get_data", return_value=(
            self.authors.merge(
                self.metadata, on="gutenberg_author_id", how="left"
            )
        )):
            ax = plot_translations()
        self.assertEqual(len(ax.patches), 3)
        self.assertEqual([bar.get_height() for bar in ax.patches], [1, 1, 1])
        with self.assertRaises(ValueError):
            plot_translations(over="alias")

    def test_modules_have_only_functions_and_imports(self):
        for path in Path("tt_gutenberg").glob("*.py"):
            tree = ast.parse(path.read_text())
            self.assertTrue(all(isinstance(node, (
                ast.FunctionDef, ast.Import, ast.ImportFrom
            )) for node in tree.body), path)


if __name__ == "__main__":
    unittest.main()
