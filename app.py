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
    "Operations & IS": [
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
}

DAYS_BACK = 14
cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)

# === APP CONFIG ===
st.set_page_config(page_title="📚 Briefcase", layout="centered")

st.title("📚 Briefcase: Academic Journal Digest")

selected_categories = st.multiselect(
    "Select categories to fetch:",
    options=list(FEEDS.keys()),
    default=list(FEEDS.keys())
)

search_query = st.text_input("🔍 Search articles (optional):")

def basic_summary(text, limit=300):
    clean = ' '.join(text.strip().split())
    if len(clean) <= limit:
        return clean
    else:
        return ' '.join(clean[:limit].split(' ')[:-1]) + "..."

def fetch_digest(selected_categories):
    feed_results = []

    for category in selected_categories:
        urls = FEEDS.get(category, [])
        for url in urls:
            parsed = feedparser.parse(url)
            journal_name = parsed.feed.get("title", "Unknown Journal")
            entries = []
            for entry in parsed.entries[:5]:
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed)) if hasattr(entry, 'published_parsed') else None
                if pub_date and pub_date >= cutoff_date:
                    entries.append({
                        "title": title,
                        "link": link,
                        "summary": summary,
                    })
            if entries:
                feed_results.append((journal_name, entries))
    return feed_results

# === MAIN ===

with st.spinner('Fetching journal entries...'):
    feed_results = fetch_digest(selected_categories)

# Building Markdown output for optional download
digest_md = f"# \ud83d\udcda Briefcase\n\n\ud83d\uddd3\ufe0f {datetime.today().strftime('%A, %B %d, %Y')}\n\n---\n"

for journal, articles in feed_results:
    st.header(f"\ud83d\udcd8\ufe0f {journal}")
    digest_md += f"## \ud83d\udcd8\ufe0f {journal}\n"
    for article in articles:
        if search_query.lower() in article["title"].lower() or search_query.lower() in article["summary"].lower():
            with st.expander(article["title"]):
                st.markdown(f"[{article['link']}]({article['link']})")
                st.write(textwrap.fill(basic_summary(article["summary"]), width=80))
            digest_md += f"- **[{article['title']}]({article['link']})**\n"
            digest_md += f"  {basic_summary(article['summary'])}\n"
    digest_md += "\n---\n"

# === DOWNLOAD BUTTON ===
st.download_button(
    label="\ud83d\udd16 Download Digest as Markdown",
    data=digest_md,
    file_name=f"briefcase_{datetime.today().strftime('%Y-%m-%d')}.md",
    mime="text/markdown"
)
