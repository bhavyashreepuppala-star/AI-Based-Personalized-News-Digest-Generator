
import sqlite3
from datetime import datetime, timezone
from difflib import SequenceMatcher

DB_NAME = "news_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_history():
    """Create the history database and table if needed."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE,
                topic TEXT,
                seen_at TEXT NOT NULL
            )
        """)


def filter_previously_seen(articles, threshold=0.88):
    """Filter articles already seen by URL or similar headline."""

    initialize_history()

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT title, url FROM seen_articles"
        ).fetchall()

    old_titles = [
        " ".join((title or "").lower().split())
        for title, _ in rows
    ]

    old_urls = {url for _, url in rows if url}

    unseen = []

    for article in articles:
        title = " ".join(
            (article.get("title") or "").lower().split()
        )
        url = article.get("url")

        if not title or title == "[removed]":
            continue

        if url and url in old_urls:
            continue

        similar = any(
            SequenceMatcher(
                None, title, old_title
            ).ratio() >= threshold
            for old_title in old_titles
        )

        if not similar:
            unseen.append(article)

    return unseen


def save_seen_articles(articles, topic):
    """Save new articles so future digests can avoid repeats."""

    initialize_history()
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        for article in articles:
            title = article.get("title") or ""
            url = article.get("url")

            if not title or not url:
                continue

            conn.execute("""
                INSERT OR IGNORE INTO seen_articles
                (title, url, topic, seen_at)
                VALUES (?, ?, ?, ?)
            """, (title, url, topic, now))


def get_history_count():
    """Return the number of saved article records."""

    initialize_history()

    with get_connection() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM seen_articles"
        ).fetchone()

    return result[0]


def clear_history():
    """Delete all previously saved article history."""

    initialize_history()

    with get_connection() as conn:
        conn.execute("DELETE FROM seen_articles")
        conn.execute(
            "DELETE FROM sqlite_sequence "
            "WHERE name = 'seen_articles'"
        )
