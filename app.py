from flask import Flask
import asyncio
import os
from naukri_scraper import scrape_naukri

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Naukri Job Scraper</title>
        </head>
        <body>
            <h1>Naukri Job Scraper</h1>
            <p>Python + Playwright Job Scraper</p>

            <form action="/scrape" method="post">
                <button type="submit">Run Naukri Scraper</button>
            </form>
        </body>
    </html>
    """


@app.route("/scrape", methods=["GET", "POST"])
def run_scraper():
    try:
        result = asyncio.run(scrape_naukri())

        return f"""
        <html>
            <head>
                <title>Scraper Result</title>
            </head>
            <body>
                <h1>Scraper Completed</h1>
                <pre>{result}</pre>
                <br>
                <a href="/">Back to Home</a>
            </body>
        </html>
        """

    except Exception as e:
        return f"""
        <html>
            <head>
                <title>Scraper Error</title>
            </head>
            <body>
                <h1>Scraper Error</h1>
                <pre>{str(e)}</pre>
                <br>
                <a href="/">Back to Home</a>
            </body>
        </html>
        """, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)