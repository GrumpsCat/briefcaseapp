#!/usr/bin/env python3

import feedparser
from datetime import datetime, timedelta
import time
import markdown as md
from datetime import timezone

# === CONFIG ===
FEEDS = {
"Business": [
    "https://journals.aom.org/action/showFeed?type=etoc&feed=rss&jc=amj",  # Academy of Management Journal (AMJ)
    "https://journals.aom.org/action/showFeed?type=etoc&feed=rss&jc=amr",  # Academy of Management Review (AMR)
    "https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=asq&type=etoc&feed=rss", # Administrative Science Quarterly (ASQ)
    "https://sms.onlinelibrary.wiley.com/feed/10970266/most-recent",  # Strategic Management Journal (SMJ)
    "https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=jom&type=etoc&feed=rss", # Journal of Management (JOM)
],
"Operations & IS": [
    "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=mnsc",  # Management Science
    "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=opre",  # Operations Research
    "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=msom",  # Manufacturing & Service Operations Management
    "https://pubsonline.informs.org/action/showFeed?type=etoc&feed=rss&jc=isre",  # Information Systems Research
],
"Higher Education": [
    "https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=uhej20",  # The Journal of Higher Education
    "https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=cshe20",  # Studies in Higher Education
    "https://campustechnology.com/rss-feeds/all-articles.aspx",                  # Campus Technology
    "https://er.educause.edu/rss",                                               # EDUCAUSE Review
    "https://www.higheredjobs.com/rss/articleFeed.cfm",                                         # HigherEdJobs - Careers
]
}

# Articles within the last X days
DAYS_BACK = 14
cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)


def parse_feed(url):
    return feedparser.parse(url)

def filter_recent_entries(entries):
    recent = []
    for entry in entries:
        if hasattr(entry, 'published_parsed'):
            pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            if pub_date >= cutoff_date:
                recent.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": pub_date.strftime('%Y-%m-%d'),
                    "summary": entry.summary if hasattr(entry, 'summary') else '',
                })
    return recent

def get_top_entries(entries, limit=5):
    top_articles = []
    for entry in entries[:limit]:
        top_articles.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", "").strip()[:300],  # Optional: truncate summary
        })
    return top_articles

def basic_summary(text, limit=300):
    """Clean and truncate summary text for display."""
    clean = text.strip().replace('\n', ' ')
    return clean[:limit] + "..." if len(clean) > limit else clean

import textwrap

def basic_summary(text, limit=300):
    """Clean and truncate summary text at word boundaries."""
    clean = ' '.join(text.strip().split())  # Remove excess whitespace
    if len(clean) <= limit:
        return clean
    else:
        return ' '.join(clean[:limit].split(' ')[:-1]) + "..."

from datetime import datetime

def write_digest_to_file(content, filename="digest.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def build_digest_output_by_journal(feed_results):
    today = datetime.today().strftime("%A, %B %d, %Y")
    lines = [f"# 📚 Briefcase\n\n📅 {today}\n\n---\n"]

    # Group articles by journal name (feed title)
    journal_articles = {}
    for (journal_name, entries) in feed_results:
        if journal_name not in journal_articles:
            journal_articles[journal_name] = []
        journal_articles[journal_name].extend(entries)

    # Sort journals alphabetically
    for journal in sorted(journal_articles):
        lines.append(f"## 📘 {journal}\n")
        for article in journal_articles[journal]:
            title = article.get("title", "Untitled").strip()
            summary = basic_summary(article.get("summary", ""))
            link = article.get("link", "#")

            line = f"- **[{title}]({link})**  "  # two spaces for line break

            # If summary looks like a citation, show it plainly
            if "Volume" in summary or "Issue" in summary or "Page" in summary:
                lines.append(f"{line}\n  {summary}")
            elif summary:
                wrapped = textwrap.fill(summary, width=80, initial_indent="  ", subsequent_indent="  ")
                lines.append(f"{line}\n{wrapped}")
            else:
                lines.append(f"{line}\n  _No summary available._")
        lines.append("\n---\n")

    return "\n".join(lines)

import os

def write_archive_index(directory=".", index_file="index.html"):
    files = sorted([
        f for f in os.listdir(directory)
        if f.startswith("digest_") and f.endswith(".html")
    ], reverse=True)

    today = datetime.today().strftime("%A, %B %d, %Y")
    lines = [f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Academic Digest Archive</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 1em; }}
    h1 {{ border-bottom: 2px solid #ccc; }}
    ul {{ padding-left: 1em; }}
    li {{ margin-bottom: 0.5em; }}
  </style>
</head>
<body>
<h1>Academic Digest Archive</h1>
<p>📅 Updated: {today}</p>
<hr>
<ul>
"""]

    for filename in files:
        date_str = filename.replace("digest_", "").replace(".html", "")
        lines.append(f'<li><a href="{filename}">{date_str}</a></li>')

    lines.append("</ul>\n</body>\n</html>")

    with open(os.path.join(directory, index_file), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))




# === MAIN ===

def write_html_output(markdown_text, output_file="digest.html"):
    html_body = md.markdown(markdown_text, extensions=["extra", "tables"])
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Academic Digest</title>
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

feed_results = []

for category, urls in FEEDS.items():
    for url in urls:
        parsed = parse_feed(url)
        journal_name = parsed.feed.get("title", "Unknown Journal")
        entries = get_top_entries(parsed.entries, limit=5)
        feed_results.append((journal_name, entries))


# Get today's date in YYYY-MM-DD format
today_str = datetime.today().strftime("%Y-%m-%d")

# File names
filename_md = f"digest_{today_str}.md"
filename_html = f"digest_{today_str}.html"

# Also write "latest" versions
latest_md = "digest.md"
latest_html = "digest.html"

# Build the digest content
markdown = build_digest_output_by_journal(feed_results)

# Write archive files
write_digest_to_file(markdown, filename_md)
write_html_output(markdown, filename_html)

# Write latest copies
write_digest_to_file(markdown, latest_md)
write_html_output(markdown, latest_html)

print(f"✅ Saved: {filename_md}, {filename_html}, and updated latest digest.md/html")

write_archive_index()
