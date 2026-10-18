
import streamlit as st

from news_fetcher import fetch_news
from deduplicator import remove_duplicates
from summarizer import summarize_article
from history import (
    filter_previously_seen,
    save_seen_articles,
    get_history_count,
    clear_history
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Personalized News Digest",
    page_icon="📰",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "articles": [],
    "topics": [],
    "summaries": {},
    "article_counts": (0, 0, 0, 0),
    "digest_generated": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📰 AI Personalized News Digest")

st.write(
    "Your personal news hub. Select multiple interests, "
    "discover new stories, avoid repetitive headlines, "
    "and generate concise AI summaries."
)

st.divider()

# --------------------------------------------------
# INTEREST SELECTION
# --------------------------------------------------

all_topics = [
    "Artificial Intelligence",
    "Technology",
    "Science",
    "Business",
    "Sports",
    "Education"
]

selected_topics = st.multiselect(
    "Choose your interests",
    all_topics,
    default=["Artificial Intelligence", "Technology", "Science"]
)

# --------------------------------------------------
# HISTORY CONTROLS
# --------------------------------------------------

history_col1, history_col2 = st.columns([3, 1])

with history_col1:
    st.caption(
        f"Stories remembered in history: {get_history_count()}"
    )

with history_col2:
    if st.button("🗑️ Clear News History"):
        clear_history()

        st.session_state.articles = []
        st.session_state.topics = []
        st.session_state.summaries = {}
        st.session_state.article_counts = (0, 0, 0, 0)
        st.session_state.digest_generated = False

        st.rerun()

# --------------------------------------------------
# FETCH PERSONALIZED NEWS
# --------------------------------------------------

if st.button("Generate My News Digest", type="primary"):

    if not selected_topics:
        st.warning("Please select at least one interest.")

    else:
        try:
            combined_articles = []
            total_fetched = 0

            with st.spinner(
                "Fetching and personalizing your news..."
            ):

                for selected_topic in selected_topics:
                    topic_articles = fetch_news(
                        selected_topic,
                        page_size=10
                    )

                    total_fetched += len(topic_articles)

                    for article in topic_articles:
                        tagged_article = article.copy()
                        tagged_article["_digest_topic"] = selected_topic
                        combined_articles.append(tagged_article)

                # Remove similar headlines across selected topics
                unique_articles = remove_duplicates(
                    combined_articles
                )

                duplicate_count = (
                    len(combined_articles) - len(unique_articles)
                )

                # Remove previously saved stories
                unseen_articles = filter_previously_seen(
                    unique_articles
                )

                previously_seen_count = (
                    len(unique_articles) - len(unseen_articles)
                )

                # Save newly discovered stories
                save_seen_articles(
                    unseen_articles,
                    ", ".join(selected_topics)
                )

                st.session_state.articles = unseen_articles
                st.session_state.topics = selected_topics.copy()

                st.session_state.article_counts = (
                    total_fetched,
                    duplicate_count,
                    previously_seen_count,
                    len(unseen_articles)
                )

                st.session_state.summaries = {}
                st.session_state.digest_generated = True

        except Exception as error:
            st.error(f"Could not generate digest: {error}")

# --------------------------------------------------
# DISPLAY PERSONALIZED DIGEST
# --------------------------------------------------

if st.session_state.digest_generated:

    (
        total_fetched,
        duplicate_count,
        previously_seen_count,
        new_count
    ) = st.session_state.article_counts

    st.subheader("Your Personalized Daily Digest")

    st.write(
        "Selected interests: "
        + ", ".join(st.session_state.topics)
    )

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Articles fetched", total_fetched)
    col2.metric("Duplicates removed", duplicate_count)
    col3.metric("Previously seen", previously_seen_count)
    col4.metric("New articles", new_count)

    st.divider()

    # --------------------------------------------------
    # CATEGORY COUNTS
    # --------------------------------------------------

    st.subheader("Articles by Category")

    category_counts = {}

    for topic in st.session_state.topics:
        category_counts[topic] = sum(
            1
            for article in st.session_state.articles
            if article.get("_digest_topic") == topic
        )

    count_columns = st.columns(
        max(1, len(st.session_state.topics))
    )

    for index, topic in enumerate(st.session_state.topics):
        count_columns[index].metric(
            topic,
            category_counts[topic]
        )

    # --------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------

    available_categories = [
        topic
        for topic in st.session_state.topics
        if category_counts[topic] > 0
    ]

    category_filter = st.selectbox(
        "Filter by category",
        ["All selected interests"] + available_categories
    )

    # --------------------------------------------------
    # CATEGORY-WISE ARTICLES
    # --------------------------------------------------

    if not st.session_state.articles:

        st.info(
            "No new stories were found for your selected interests. "
            "Try different topics or clear history to test again."
        )

    else:

        for category in st.session_state.topics:

            if (
                category_filter != "All selected interests"
                and category_filter != category
            ):
                continue

            category_articles = [
                (index, article)
                for index, article in enumerate(
                    st.session_state.articles
                )
                if article.get("_digest_topic") == category
            ]

            if not category_articles:
                continue

            st.header(f"📂 {category}")

            for index, article in category_articles:

                title = (
                    article.get("title")
                    or "Untitled article"
                )

                description = (
                    article.get("description")
                    or "No description available."
                )

                source_info = article.get("source") or {}

                source = (
                    source_info.get("name")
                    or "Unknown source"
                )

                published_at = (
                    article.get("publishedAt")
                    or "Date unavailable"
                )

                article_url = article.get("url")

                summary_key = f"{index}_{title}"

                with st.container(border=True):

                    st.caption(
                        f"📰 {source} | Published: {published_at}"
                    )

                    st.subheader(title)
                    st.write(description)

                    if article_url:
                        st.markdown(
                            f"[Read full article]({article_url})"
                        )

                    # AI summary button
                    if st.button(
                        "✨ Generate AI Summary",
                        key=f"summary_button_{index}"
                    ):

                        with st.spinner(
                            "Generating AI summary..."
                        ):
                            summary = summarize_article(
                                title,
                                description
                            )

                            st.session_state.summaries[
                                summary_key
                            ] = summary

                    # Display AI summary or friendly API message
                    if summary_key in st.session_state.summaries:

                        summary = st.session_state.summaries[
                            summary_key
                        ]

                        st.markdown("### 🤖 AI Summary")

                        if summary.startswith(
                            "AI summary temporarily unavailable"
                        ):
                            st.warning(summary)

                        elif summary.startswith(
                            "Gemini's request quota"
                        ):
                            st.warning(summary)

                        elif summary.startswith(
                            "AI summaries are unavailable"
                        ):
                            st.info(summary)

                        elif summary.startswith(
                            "Could not generate"
                        ):
                            st.warning(summary)

                        else:
                            st.write(summary)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Personalized News Digest | Multiple interests | "
    "News fetching | Duplicate detection | Persistent history | "
    "AI summarization"
)
