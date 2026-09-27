import asyncio
import logging
import os
import re

import pandas as pd
from playwright.async_api import async_playwright


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://www.naukri.com/python-developer-jobs"
EXCEL_FILE = "naukri_jobs.xlsx"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def clean_text(text):
    """Remove unnecessary spaces from text."""

    if not text:
        return ""

    return " ".join(text.split())


# ============================================================
# EXTRACT JOB ID
# ============================================================

def extract_job_id(url):
    """Extract a Naukri job ID from the job URL."""

    if not url:
        return ""

    # Naukri URLs commonly contain job IDs such as
    # /job-listings-python-developer-...-123456789
    match = re.search(r"-(\d{6,})", url)

    if match:
        return match.group(1)

    return url


# ============================================================
# EXTRACT JOB INFORMATION
# ============================================================

async def extract_job(card):

    try:

        # -------------------------------
        # Job title
        # -------------------------------

        title_locator = card.locator(
            "a.title"
        )

        if await title_locator.count() > 0:

            title = clean_text(
                await title_locator.first.inner_text()
            )

            job_url = await title_locator.first.get_attribute(
                "href"
            )

        else:

            title = ""
            job_url = ""

        # -------------------------------
        # Company
        # -------------------------------

        company_locator = card.locator(
            "a.comp-name"
        )

        if await company_locator.count() > 0:

            company = clean_text(
                await company_locator.first.inner_text()
            )

        else:

            company = ""

        # -------------------------------
        # Location
        # -------------------------------

        location_locator = card.locator(
            ".locWdth"
        )

        if await location_locator.count() > 0:

            location = clean_text(
                await location_locator.first.inner_text()
            )

        else:

            location = ""

        # -------------------------------
        # Experience
        # -------------------------------

        experience_locator = card.locator(
            ".expwdth"
        )

        if await experience_locator.count() > 0:

            experience = clean_text(
                await experience_locator.first.inner_text()
            )

        else:

            experience = ""

        # -------------------------------
        # Complete card text
        # -------------------------------

        card_text = clean_text(
            await card.inner_text()
        )

        # -------------------------------
        # Posted date
        # -------------------------------

        posted_date = ""

        date_patterns = [
            r"\b\d+\s+day[s]?\s+ago\b",
            r"\b\d+\s+week[s]?\s+ago\b",
            r"\b\d+\s+hour[s]?\s+ago\b",
            r"\b\d+\s+month[s]?\s+ago\b",
            r"\bToday\b",
            r"\bYesterday\b",
            r"\b\d{1,2}\s+[A-Za-z]{3}\b"
        ]

        for pattern in date_patterns:

            match = re.search(
                pattern,
                card_text,
                re.IGNORECASE
            )

            if match:

                posted_date = match.group(0)
                break

        # -------------------------------
        # Skills
        # -------------------------------

        skills_locator = card.locator(
            ".tags-gt"
        )

        if await skills_locator.count() > 0:

            skills = clean_text(
                await skills_locator.first.inner_text()
            )

        else:

            skills = ""

        # -------------------------------
        # Job ID
        # -------------------------------

        job_id = extract_job_id(job_url)

        return {
            "Job ID": job_id,
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Experience": experience,
            "Skills": skills,
            "Posted Date": posted_date,
            "Job URL": job_url
        }

    except Exception as e:

        logging.exception(
            "Error extracting job: %s",
            e
        )

        return None


# ============================================================
# SAVE NEW JOBS TO EXCEL
# ============================================================

def save_jobs_to_excel(jobs):

    if not jobs:

        print("No jobs found.")
        return

    new_df = pd.DataFrame(jobs)

    # --------------------------------------------------------
    # Remove duplicate jobs from current scraping
    # --------------------------------------------------------

    new_df = new_df.drop_duplicates(
        subset=["Job URL"]
    )

    # --------------------------------------------------------
    # Read existing Excel file
    # --------------------------------------------------------

    if os.path.exists(EXCEL_FILE):

        try:

            existing_df = pd.read_excel(
                EXCEL_FILE
            )

            print(
                f"Existing jobs in Excel: {len(existing_df)}"
            )

        except Exception as e:

            logging.exception(
                "Could not read Excel file: %s",
                e
            )

            existing_df = pd.DataFrame()

    else:

        existing_df = pd.DataFrame()

    # --------------------------------------------------------
    # Find new jobs
    # --------------------------------------------------------

    if not existing_df.empty:

        existing_urls = set(
            existing_df["Job URL"]
            .dropna()
            .astype(str)
        )

        new_df = new_df[
            ~new_df["Job URL"].astype(str).isin(
                existing_urls
            )
        ]

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    if new_df.empty:

        print("No new jobs found.")
        logging.info("No new jobs found.")

        return

    final_df = pd.concat(
        [existing_df, new_df],
        ignore_index=True
    )

    final_df = final_df.drop_duplicates(
        subset=["Job URL"],
        keep="first"
    )

    final_df.to_excel(
        EXCEL_FILE,
        index=False
    )

    print(
        f"New jobs added: {len(new_df)}"
    )

    print(
        f"Total jobs in Excel: {len(final_df)}"
    )

    logging.info(
        "Added %s new jobs",
        len(new_df)
    )


# ============================================================
# MAIN SCRAPER
# ============================================================

async def scrape_naukri():

    logging.info(
        "Starting Naukri scraper"
    )

    jobs = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        try:

            print("Opening Naukri...")

            await page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(
                5000
            )

            print(
                "Page loaded successfully."
            )

            print(
                "Page title:",
                await page.title()
            )

            # ------------------------------------------------
            # Find job cards
            # ------------------------------------------------

            job_cards = page.locator(
                "div.srp-jobtuple-wrapper"
            )

            count = await job_cards.count()

            print(
                f"Job cards found: {count}"
            )

            logging.info(
                "Job cards found: %s",
                count
            )

            # ------------------------------------------------
            # Extract jobs
            # ------------------------------------------------

            for i in range(count):

                card = job_cards.nth(i)

                job = await extract_job(
                    card
                )

                if job:

                    jobs.append(job)

                    print(
                        f"Scraped job {i + 1}: "
                        f"{job['Job Title']}"
                    )

            # ------------------------------------------------
            # Save to Excel
            # ------------------------------------------------

            print(
                "\nSaving jobs to Excel..."
            )

            save_jobs_to_excel(
                jobs
            )

            print(
                "\nScraping completed successfully."
            )

        except Exception as e:

            print(
                "Error:",
                e
            )

            logging.exception(
                "Scraper error: %s",
                e
            )

        finally:

            await browser.close()

            logging.info(
                "Browser closed"
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    asyncio.run(
        scrape_naukri()
    )
