import pandas as pd
import seaborn as sns

from tt_gutenberg.transform import get_data, plot_prep


def list_authors(by_languages=False, alias=False):
    """List author names or nonmissing aliases, optionally ranked by languages.

    Languages are counted once per author, even when many books share them.
    Authors with no recorded language receive zero. Ties retain source order.
    """
    authors = get_data()
    column = "author_alias" if alias else "author"
    if "alias" in authors.columns and "author_alias" not in authors.columns:
        authors = authors.rename(columns={"alias": "author_alias"})
    if column not in authors.columns:
        authors = authors.reset_index()
    if by_languages:
        if pd.api.types.is_numeric_dtype(authors["language"]):
            counts = authors.groupby(column, sort=False)["language"].max()
        else:
            authors["language"] = authors["language"].str.split("/")
            authors = authors.explode("language")
            authors["language"] = authors["language"].str.strip()
            counts = authors.groupby(column, sort=False)["language"].nunique()
        authors = authors.drop_duplicates(column).copy()
        authors["translation_count"] = authors[column].map(counts)
    names = authors[column].str.strip()
    authors = authors.loc[names.notna() & names.ne("")].copy()
    authors[column] = names.loc[authors.index]
    if by_languages:
        authors = authors.sort_values(
            "translation_count", ascending=False, kind="stable"
        )
    return authors[column].tolist()


def plot_translations(over="birth_century"):
    """Plot mean languages per author with a 95% bootstrap interval."""
    if over != "birth_century":
        raise ValueError("over must be 'birth_century'")
    authors = plot_prep(over=over)
    with sns.axes_style("whitegrid"):
        ax = sns.barplot(
            data=authors,
            x=over,
            y="language",
            order=sorted(authors[over].unique()),
            estimator="mean",
            errorbar=("ci", 95),
            seed=501,
            color="steelblue",
        )
    ax.set(
        xlabel="Birth century (starting year)",
        ylabel="Mean number of distinct languages per author",
    )
    ax.set_title("Translation Count Over Birth Century")
    ax.tick_params(axis="x", rotation=90)
    ax.figure.set_size_inches(12, 5)
    ax.figure.tight_layout()
    return ax
