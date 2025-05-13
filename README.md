# 📚 BriefCase: The Academic Journal Aggregator

**BriefCase** is a simple, automated tool that fetches and displays the latest academic journal articles from top publications in **Business**, **Operations & Information Systems**, and **Higher Education**. It runs automatically, updates four times a day, and is deployed via [GitHub Pages](https://grumpscat.github.io/briefcaseapp/).

---

## 🔍 Features

- Aggregates article metadata from academic RSS feeds
- Groups articles by journal
- Displays summaries and links in a clean single-page format
- Labels each update as "Morning / Afternoon / Evening / Late Evening Edition"
- Automatically updates via GitHub Actions
- Free and hosted using GitHub Pages

---

## 🌐 Live Site

👉 [https://grumpscat.github.io/briefcaseapp/](https://grumpscat.github.io/briefcaseapp/)

---

## 🛠️ How It Works

1. `briefcaseapp.py` pulls RSS feeds and builds a Markdown digest
2. Converts it to a styled HTML page (`index.html`)
3. GitHub Actions runs the script on a schedule or manually
4. Output is committed and served as a GitHub Pages site

---

## 🕓 Edition Times

- **Morning Edition** – 5:00–11:59 UTC
- **Afternoon Edition** – 12:00–16:59 UTC
- **Evening Edition** – 17:00–20:59 UTC
- **Late Evening Edition** – 21:00–04:59 UTC

---

## 📁 Project Structure


