#!/usr/bin/env python3

import feedparser
import os
import time
import textwrap
import markdown as md
from datetime import datetime, timedelta, timezone
import pytz

# === TIMEZONE SETUP ===
local_tz = pytz.timezone('America/Los_Angeles')
now = datetime.now(local_tz)
cutoff_date = datetime.now(timezone.utc) - timedelta(days=14)

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
    ]
}

# === UTILITIES ===

def parse_feed(url):
    return feedparser.parse(url)

def get_top_entries(entries, limit=5):
    top_articles = []
    for entry in entries[:limit]:
        top_articles.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", "").strip()[:300],
        })
    return top_articles

def basic_summary(text, limit=300):
    clean = ' '.join(text.strip().split())
    if len(clean) <= limit:
        return clean
    else:
        return ' '.join(clean[:limit].split(' ')[:-1]) + "..."

def get_edition_label(current_time):
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Morning Edition"
    elif 12 <= hour < 17:
        return "Afternoon Edition"
    elif 17 <= hour < 21:
        return "Evening Edition"
    else:
        return "Late Evening Edition"

def build_digest_output_by_journal(feed_results, current_time):
    edition_label = get_edition_label(current_time)
    today = current_time.strftime("%A, %B %d, %Y")
    edition_line = f"{edition_label} of {today}"

    lines = [f"# 📚 BriefCase: The Academic Journal Aggregator\n\n📅 {edition_line}\n\n---\n"]

    journal_articles = {}
    for (journal_name, entries) in feed_results:
        if journal_name not in journal_articles:
            journal_articles[journal_name] = []
        journal_articles[journal_name].extend(entries)

    for journal in sorted(journal_articles):
        lines.append(f"## 📘 {journal}\n")
        for article in journal_articles[journal]:
            title = article.get("title", "Untitled").strip()
            summary = basic_summary(article.get("summary", ""))
            link = article.get("link", "#")

            line = f"- **[{title}]({link})**"

            if "Volume" in summary or "Issue" in summary or "Page" in summary:
                lines.append(f"{line}\n  {summary}")
            elif summary:
                wrapped = textwrap.fill(summary, width=80, initial_indent="  ", subsequent_indent="  ")
                lines.append(f"{line}\n{wrapped}")
            else:
                lines.append(f"{line}\n  _No summary available._")
        lines.append("\n---\n")

    return "\n".join(lines)

def write_html_output(markdown_text, output_file="index.html"):
    html_body = md.markdown(markdown_text, extensions=["extra", "tables"])
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BriefCase: The Academic Journal Aggregator</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 1em; }}
    h1, h2 {{ color: #333; }}
    a {{ color: #0645AD; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    hr {{ margin: 2em 0; }}
    .summary {{ color: #555; font-style: italic; }}
  </style>
</head>
<body>
{html_body}
</body>
</html>"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)

# === MAIN EXECUTION ===

print("🕒 Now:", now.isoformat())

feed_results = []

for category, urls in FEEDS.items():
    for url in urls:
        parsed = parse_feed(url)
        journal_name = parsed.feed.get("title", "Unknown Journal")
        entries = get_top_entries(parsed.entries, limit=5)
        feed_results.append((journal_name, entries))

# Build and write the latest edition as index.html
markdown_text = build_digest_output_by_journal(feed_results, now)
write_html_output(markdown_text, "index.html")

print("✅ Updated: index.html (latest edition only)")
