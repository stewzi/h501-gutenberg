import seaborn as sns

from tt_gutenberg.transform import birth_centuries, count_languages, load_data


def list_authors(by_languages=False, alias=False):
    """List author names or nonmissing aliases, optionally ranked by languages.

    Languages are counted once per author, even when many books share them.
    Authors with no recorded language receive zero. Ties retain source order.
    """
    authors, metadata = load_data()
    authors = count_languages(authors, metadata)
    column = "alias" if alias else "author"
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
    authors, metadata = load_data()
    authors = birth_centuries(count_languages(authors, metadata))
    authors = authors.drop_duplicates("gutenberg_author_id")
    with sns.axes_style("whitegrid"):
        ax = sns.barplot(
            data=authors,
            x=over,
            y="translation_count",
            order=sorted(authors[over].unique()),
            estimator="mean",
            errorbar=("ci", 95),
            seed=501,
            color="steelblue",
        )
    ax.set(
        xlabel="Birth century (starting year)",
        ylabel="Mean number of distinct languages per author",
        title="Project Gutenberg languages by author birth century",
    )
    ax.tick_params(axis="x", rotation=90)
    ax.figure.set_size_inches(12, 5)
    ax.figure.tight_layout()
    return ax
