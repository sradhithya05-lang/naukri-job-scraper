import asyncio
import logging
import os
import re

import pandas as pd
from playwright.async_api import async_playwright


BASE_URL = "https://www.naukri.com/python-developer-jobs"
EXCEL_FILE = "naukri_jobs.xlsx"


logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_text(text):
    if not text:
        return ""

    return " ".join(text.split())


def extract_job_id(url):
    if not url:
        return ""

    match = re.search(r"-(\d{6,})", url)

    if match:
        return match.group(1)

    return url
async def extract_job(card):
    try:
        title = ""
        company = ""
        location = ""
        experience = ""
        skills = ""
        posted_date = ""
        job_url = ""

        title_element = card.locator("a.title").first
        if await title_element.count() > 0:
            title = clean_text(await title_element.inner_text())
            job_url = await title_element.get_attribute("href") or ""

        company_element = card.locator("a.comp-name").first
        if await company_element.count() > 0:
            company = clean_text(await company_element.inner_text())

        location_element = card.locator(".locWdth").first
        if await location_element.count() > 0:
            location = clean_text(await location_element.inner_text())

        experience_element = card.locator(".expwdth").first
        if await experience_element.count() > 0:
            experience = clean_text(await experience_element.inner_text())

        skills_element = card.locator(".tags-gt").first
        if await skills_element.count() > 0:
            skills = clean_text(await skills_element.inner_text())

        posted_element = card.locator(".job-post-day").first
        if await posted_element.count() > 0:
            posted_date = clean_text(await posted_element.inner_text())

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
        logging.error("Error extracting job: %s", e)
        return None
def save_jobs_to_excel(jobs):
    if not jobs:
        print("No jobs to save.")
        return

    try:
        if os.path.exists(EXCEL_FILE):
            existing_df = pd.read_excel(EXCEL_FILE)
        else:
            existing_df = pd.DataFrame()

        new_df = pd.DataFrame(jobs)

        if existing_df.empty:
            final_df = new_df
            new_jobs_count = len(new_df)

        else:
            existing_urls = set(
                existing_df["Job URL"].dropna().astype(str)
            )

            new_df = new_df[
                ~new_df["Job URL"].astype(str).isin(existing_urls)
            ]

            new_jobs_count = len(new_df)

            if new_df.empty:
                final_df = existing_df
            else:
                final_df = pd.concat(
                    [existing_df, new_df],
                    ignore_index=True
                )

        final_df.to_excel(EXCEL_FILE, index=False)

        print(f"Existing jobs in Excel: {len(existing_df)}")
        print(f"New jobs added: {new_jobs_count}")
        print(f"Total jobs in Excel: {len(final_df)}")

        logging.info(
            "Excel updated. New jobs: %s, Total jobs: %s",
            new_jobs_count,
            len(final_df)
        )

    except Exception as e:
        logging.error("Error saving Excel file: %s", e)
        print(f"Error saving Excel file: {e}")
async def scrape_naukri():
    print("Opening Naukri...")

    jobs = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
               headless=False,
               args=[
        "--disable-blink-features=AutomationControlled"
    ]
)

            page = await browser.new_page()

            await page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("Page loaded successfully.")
            print("Page title:", await page.title())
            print("Current URL:", page.url)

            await page.wait_for_timeout(15000)

            print("Page text:", (await page.locator("body").inner_text())[:1000])

            cards = page.locator("div.srp-jobtuple-wrapper")

            job_count = await cards.count()

            print(f"Job cards found: {job_count}")

            for i in range(job_count):
                job = await extract_job(cards.nth(i))

                if job and job.get("Job URL"):
                    jobs.append(job)
                    print(
                        f"Scraped job {len(jobs)}: "
                        f"{job.get('Job Title', '')}"
                    )

            print(f"Jobs scraped: {len(jobs)}")

            await browser.close()

        if jobs:
            save_jobs_to_excel(jobs)
        else:
            print("No jobs found.")

        print("Scraping completed successfully.")

        return (
            f"Job cards found: {job_count}\n"
            f"Jobs scraped: {len(jobs)}\n"
            f"Scraping completed successfully."
        )

    except Exception as e:
        logging.error("Scraper error: %s", e)
        print(f"Scraper error: {e}")
        raise
if __name__ == "__main__":
    asyncio.run(scrape_naukri())