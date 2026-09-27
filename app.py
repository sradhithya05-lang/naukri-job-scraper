from flask import Flask
import subprocess
import sys
import os

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Naukri Job Scraper</h1>
    <p>Application deployed successfully on Railway.</p>
    <p><a href="/scrape">Run Naukri Scraper</a></p>
    """


@app.route("/scrape")
def run_scraper():
    try:
        subprocess.Popen(
            [sys.executable, "-u", "naukri_scraper.py"]
        )

        return """
        <h1>Scraper Started</h1>
        <p>The Naukri scraper has been started.</p>
        <p>Check Railway logs for the scraping progress.</p>
        """

    except Exception as e:
        return f"""
        <h1>Scraper Error</h1>
        <p>{str(e)}</p>
        """, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )