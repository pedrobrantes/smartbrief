# SmartBrief

> **A personal Python automation script.**
> Generates a daily email with a financial snapshot, news, and highlights, using AI solely for text synthesis.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Build](https://img.shields.io/github/actions/workflow/status/pedrobrantes/smartbrief/daily.yml?label=Daily%20Briefing)
![License](https://img.shields.io/badge/License-MIT-green)

## What is this?

**SmartBrief** is a simple tool I built to avoid opening 5 different websites every morning. It runs automatically once a day, collects raw data from trusted sources, and emails me a formatted briefing.

It is not a complex "Operating System." It is a well-structured script that:
1.  Downloads financial quotes (Yahoo Finance).
2.  Fetches recent news on topics I care about (Google News).
3.  Asks Google Gemini to provide a quick summary (so I don't have to read long texts).
4.  Assembles a clean HTML email and sends it to my inbox.

## Features

* **AI Summary:** Uses the Gemini Flash model (free/fast tier) to write a paragraph about the market and headlines.
* **Financial Tracking:** A simple table with asset variations (USD, BTC, Stocks) and mini-charts (sparklines) of the last 7 days.
* **Filtered News:** Actively hunts for specific keywords (e.g., Rust, Linux) instead of just reading a generic feed.
* **Trends:** Shows what is being searched in Google Brazil (or falls back to interest topics if the API blocks the request).
* **Responsive Design:** The email renders perfectly on mobile and desktop (built with MJML).

## Tech Stack

* **Python 3.11** + **uv** (Package manager)
* **yfinance** (Market data)
* **feedparser** (News RSS)
* **Google Gemini API** (Text summarization)
* **QuickChart** (Static image generation for charts)
* **MJML** (Email templating)

## How to Run

### 1. Install
You need Python and `uv` (or pip).

If you have nix, run:
```bash
nix flake update
nix develop
```
and
```bash
git clone [https://github.com/pedrobrantes/smartbrief.git](https://github.com/pedrobrantes/smartbrief.git)
cd smartbrief
uv sync  # or: pip install -r requirements.txt
```

### 2. Configuration

Create a .env file in the root directory or Github Actions Secrets:
RESEND_API_KEY=re_123...       # Get at resend.com
EMAIL_TO=your@email.com
GEMINI_API_KEY=AIzaSy...       # Get at aistudio.google.com

### 3. Run Manually

```bash
uv run src/main.py
```

### 4. Customization

Edit src/settings.py to change:
 * TICKERS: Stocks and currencies you want to track.
 * KEYWORDS: News topics the script should search for.
 * CHART_THEME: Email colors.

### 5. Automation

The project includes a .github/workflows/daily.yml file. If you fork this repository and add your keys to GitHub Secrets, it will run automatically every weekday at 07:00 AM.
