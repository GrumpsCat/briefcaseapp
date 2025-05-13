import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
import time
import textwrap
import io

# === CONFIG ===
FEEDS = {
    "Business": [
        "https://journals.aom.org/action/showFeed?type=etoc&feed=rss&jc=amj",
        "https://journals.aom.org/action/showFeed?type=etoc&feed=rss&jc=amr",
        "https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=asq&type=etoc&feed=rss",
        "https://sms.onlinelibrary.wiley.com/feed/10970266/most-recent",
        "https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=jom&type=etoc&feed=rss",
    ],
    "Operations & Information Systems": [
        "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=mnsc",
        "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=opre",
        "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=msom",
        "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=isre",
    ],
    "Higher Education": [
        "https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=uhej20",
        "https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=cshe20",
        "https://campustechnology.com/rss-feeds/all-articles.aspx",
        "https://er.educause.edu/rss",
        "https://www.higheredjobs.com/rss/articleFeed.cfm",
    ],
    "Technology & Innovation": [
        "https://www.technologyreview.com/feed/",
        "https://spectrum.ieee.org/rss/fulltext",
    ],
    "Public Policy": [
        "https://www.educationnext.org/feed/",
        "https://www.insidehighered.com/news/feed",
        "https://www.epi.org/blog/feed/",
        "https://www.pewresearch.org/feed/",
        "https://www.urban.org/rss.xml",
        "https://www.nber.org/rss/news",
    ],
}

CATEGORY_EMOJIS = {
    "Business": "💼",
    "Operations & Information Systems": "🛠️",
    "Higher Education": "🎓",
    "Technology & Innovation": "🧪",
    "Public Policy": "🏛️",
}

# === APP CONFIG ===
st.set_page_config(page_title="📚 Briefcase", layout="centered")

st.title("📚 Briefcase: Academic Journal Digest")

selected_categories = st.multiselect(
    "Select categories to fetch:",
    options=list(FEEDS.keys()),
    default=list(FEEDS.keys())
)

search_query = st.text_input("🔍 Search articles (optional):")

# Show last refreshed time
last_refresh_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
st.caption(f"Last refreshed: {last_refresh_time}")

article_limit = st.slider("How many articles per journal?", min_value=1, max_value=15, value=5)

def basic_summary(text, limit=300):
    clean = ' '.join(text.strip().split())
    if len(clean) <= limit:
        return clean
    else:
        return ' '.join(clean[:limit].split(' ')[:-1]) + "..."

def fetch_digest(selected_categories, article_limit):
    feed_results = {}

    for category in selected_categories:
        urls = FEEDS.get(category, [])
        category_entries = []
        for url in urls:
            parsed = feedparser.parse(url)
            journal_name = parsed.feed.get("title", "Unknown Journal")
            entries = []
            for entry in parsed.entries[:article_limit]:
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                published = ""
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime.fromtimestamp(time.mktime(entry.published_parsed)).strftime('%B %d, %Y')

                entries.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                })
            if entries:
                category_entries.append((journal_name, entries))
        if category_entries:
            feed_results[category] = category_entries

    return feed_results

# === MAIN ===

with st.spinner('Fetching journal entries...'):
    feed_results = fetch_digest(selected_categories, article_limit)

# Building Markdown output for optional download
digest_md = f"# 📚 Briefcase\n\n🗓️ {datetime.today().strftime('%A, %B %d, %Y')}\n\n---\n"

for category, journals in feed_results.items():
    emoji = CATEGORY_EMOJIS.get(category, "📂")
    st.subheader(f"{emoji} {category}")
    digest_md += f"# {emoji} {category}\n"

    for journal, articles in journals:
        st.header(f"📘 {journal}")
        digest_md += f"## 📘 {journal}\n"
        for article in articles:
            if search_query.lower() in article["title"].lower() or search_query.lower() in article["summary"].lower():
                display_title = article['title']
                if article['published']:
                    display_title += f" ({article['published']})"
                with st.expander(display_title):
                    st.markdown(f"[{article['link']}]({article['link']})")
                    st.write(textwrap.fill(basic_summary(article["summary"]), width=80))
                digest_md += f"- **[{article['title']}]({article['link']})**"
                if article['published']:
                    digest_md += f" ({article['published']})"
                digest_md += "\n"
                digest_md += f"  {basic_summary(article['summary'])}\n"
        digest_md += "\n---\n"

# === DOWNLOAD BUTTON ===
st.download_button(
    label="🔗 Download Digest as Markdown",
    data=digest_md,
    file_name=f"briefcase_{datetime.today().strftime('%Y-%m-%d')}.md",
    mime="text/markdown"
)
