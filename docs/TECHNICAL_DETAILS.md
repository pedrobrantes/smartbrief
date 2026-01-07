# How it Works (Technical Details)

A simple explanation of how the script processes data and sends the email.

## Execution Flow

The script runs linearly (step-by-step):

1.  **Collectors:**
    * Accesses Yahoo Finance to get the current price and 7-day history.
    * Accesses Google News RSS, filtering by the keywords defined in `settings.py`.
    * Attempts to access Google Trends. If Google blocks the request (which is common for scripts), it uses a default list of interests (Fallback) to ensure the UI doesn't break.

2.  **Processing (Agents):**
    * The script assembles a simple text string with the collected data.
    * It sends this text to the Google Gemini API with a prompt: "Summarize this in 2 paragraphs and give me a word of the day."
    * If the API fails (rate limits), the script tries a simpler model or uses default text, ensuring the email is always sent.

3.  **Visualization:**
    * The script does **not** generate charts on your computer. It constructs a URL for **QuickChart.io** (an open API) which returns a PNG image.
    * This keeps the script very lightweight, as it doesn't need to install heavy plotting libraries like matplotlib.

4.  **Assembly (Template):**
    * We use **MJML** to create the email layout. It is a language that "compiles" into HTML compatible with Gmail and Outlook.
    * Python substitutes the placeholders `{{ title }}` with real data (using Jinja2).

5.  **Delivery:**
    * The final HTML with design inspired in Material You is sent via the **Resend** API (free tier is sufficient for personal use).

## Folder Structure

* `src/main.py`: The main entry point that orchestrates everything.
* `src/settings.py`: Configuration file (tickers, colors, icons).
* `src/collectors/`: Scripts that fetch data from the internet.
* `src/agents/`: Logic for calling the AI.
* `src/templates/`: The email layout file (.mjml).
* `tests/`: Basic tests to ensure nothing is broken before running.
