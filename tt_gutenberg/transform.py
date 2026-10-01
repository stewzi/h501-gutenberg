import pandas as pd


def load_data():
    """Read the fixed TidyTuesday snapshot of authors and book metadata."""
    base = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/"
    )
    authors = pd.read_csv(base + "gutenberg_authors.csv")
    metadata = pd.read_csv(base + "gutenberg_metadata.csv")
    return authors, metadata


def count_languages(authors, metadata):
    """Attach each author's number of distinct languages across all works."""
    languages = metadata[["gutenberg_author_id", "language"]].copy()
    languages["language"] = languages["language"].str.split("/")
    languages = languages.explode("language")
    languages["language"] = languages["language"].str.strip()
    languages = languages.loc[languages["language"].ne("")]
    counts = languages.groupby("gutenberg_author_id")["language"].nunique()
    counts = counts.rename("translation_count")
    result = authors.merge(
        counts, on="gutenberg_author_id", how="left", validate="many_to_one"
    )
    result["translation_count"] = (
        result["translation_count"].fillna(0).astype(int)
    )
    return result


def birth_centuries(authors):
    """Remove unknown birth years and floor years to century starts."""
    result = authors.copy()
    result["birthdate"] = pd.to_numeric(result["birthdate"], errors="coerce")
    result = result.dropna(subset=["birthdate"])
    result["birth_century"] = (result["birthdate"] // 100 * 100).astype(int)
    return result
