
from difflib import SequenceMatcher


def normalize_title(title):
    """Convert a headline to lowercase and normalize spaces."""
    return " ".join((title or "").lower().split())


def remove_duplicates(articles, threshold=0.85):
    """Remove articles with identical or highly similar headlines."""

    unique_articles = []
    seen_titles = []

    for article in articles:
        title = normalize_title(article.get("title"))

        # Skip missing or removed headlines
        if not title or title == "[removed]":
            continue

        duplicate = False

        for existing_title in seen_titles:
            similarity = SequenceMatcher(
                None,
                title,
                existing_title
            ).ratio()

            if similarity >= threshold:
                duplicate = True
                break

        if not duplicate:
            unique_articles.append(article)
            seen_titles.append(title)

    return unique_articles
