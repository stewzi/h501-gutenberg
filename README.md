# h501-gutenberg

Week 4 Gutenberg author analysis using Python modules, pandas, and Seaborn.
Data source: [TidyTuesday 2025-06-03](https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-06-03/readme.md).

## Environment (Python 3.12, venv)

```sh
python3.12 -m venv --prompt h501-gutenberg .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name h501-gutenberg --display-name "Python (h501-gutenberg)"
```

Open `gutenberg.ipynb` in VS Code and select **Python (h501-gutenberg)**.
The first cell runs `conda env list` as required by the exercise; the next cell
shows that the actual notebook uses this project's venv. Conda does not list
venvs. An internet connection is needed to read the original CSV files.

## Package

- `tt_gutenberg/authors.py`: public list and plot functions.
- `tt_gutenberg/transform.py`: data loading, distinct language counts, centuries.
- `tt_gutenberg/__init__.py`: package exports.
- `tests/`: local edge-case and package-structure checks.

`list_authors(by_languages=True, alias=True)` excludes missing/blank aliases
and returns aliases ordered by decreasing distinct language count. Duplicate
books in the same language do not inflate counts. Multilingual works are split
on `/`; missing languages are excluded. Ties preserve author dataset order.
The original language is included because the dataset does not distinguish it
from translations. The chart uses authors, including those without aliases,
and displays 95% bootstrap confidence intervals (fixed random seed).

```sh
python -m unittest discover -s tests -v
python -m pycodestyle tt_gutenberg tests
```

## Submission

Use the **GitHub** method for Week 4 on Gradescope and select this repository's
`main` branch. After all Gradescope tests pass, submit this repository's public
URL to the Canvas coding exercise. Complete your own self-assessment and Week 4
metacognitive report in Canvas. Local tests do not replace the Gradescope tests.
