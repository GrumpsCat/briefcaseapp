#!/usr/bin/env python3

import feedparser
from datetime import datetime, timedelta, timezone
import pytz
import os

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

# === HELPERS ===

def parse_feed(url):
    return feedparser.parse(url)

def get_top_entries(entries, limit=5):
    top_articles = []
    for entry in entries[:limit]:
        top_articles.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", "#"),
            "summary": entry.get("summary", "").strip(),
        })
    return top_articles

def extract_citation(summary):
    """Try to extract a likely citation line from the summary."""
    lines = summary.split(". ")
    for line in lines:
        if any(keyword in line for keyword in ["Volume", "Issue", "Page", "DOI"]):
            return line.strip()
    return ""

def build_digest_html(feed_results, current_time):
    edition_label = get_edition_label(current_time)
    today = current_time.strftime("%A, %B %d, %Y")
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    html = [f"<h1>📚 BriefCase: The Academic Journal Aggregator</h1>",
            f"<p>📅 <strong>{edition_label} of {today}</strong> — <em>{timestamp}</em></p><hr>"]

    journal_articles = {}
    for (journal_name, entries) in feed_results:
        if journal_name not in journal_articles:
            journal_articles[journal_name] = []
        journal_articles[journal_name].extend(entries)

    for journal in sorted(journal_articles):
        html.append(f"<h2>📘 {journal}</h2>")
        for article in journal_articles[journal]:
            title = article["title"]
            link = article["link"]
            summary = article["summary"]

            citation = extract_citation(summary)
            clean_summary = summary.replace(citation, "").strip()

            html.append("<div style='margin-bottom: 1.5em;'>")
            html.append(f"<p><strong><a href='{link}'>{title}</a></strong></p>")
            if citation:
                html.append(f"<p><em>{citation}</em></p>")
            if clean_summary:
                html.append(f"<p>{clean_summary}</p>")
            html.append("</div>")

        html.append("<hr>")

    return "\n".join(html)

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

def write_html_output(html_content, output_file="index.html"):
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
    .summary {{ color: #555; }}
  </style>
</head>
<body>
{html_content}
</body>
</html>"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)

# === MAIN EXECUTION ===

print("🕒 Running at", now.isoformat())

# Proof of execution
with open("proof-it-ran.txt", "w") as f:
    f.write(f"✅ Ran at {now.isoformat()}\n")

feed_results = []

for category, urls in FEEDS.items():
    for url in urls:
        parsed = parse_feed(url)
        journal_name = parsed.feed.get("title", "Unknown Journal")
        entries = get_top_entries(parsed.entries, limit=5)
        feed_results.append((journal_name, entries))

html_output = build_digest_html(feed_results, now)
write_html_output(html_output, "index.html")

print("✅ Digest written to index.html")
