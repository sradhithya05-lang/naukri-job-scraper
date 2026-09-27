# Naukri Job Scraper Using Python & Playwright

## 1. Project Overview

This project is a Python-based web scraper developed using Playwright to collect job listing information from Naukri.com.

The scraper searches for Python Developer jobs and extracts:

* Job Title
* Company Name
* Location
* Experience
* Skills
* Posted Date
* Job URL

The collected job information is stored in an Excel file.

On every new run, the scraper compares newly scraped jobs with the existing records and adds only new jobs.

---

## 2. Features

* Scrapes Python Developer job listings from Naukri.com
* Extracts job title, company, location, experience, skills, posted date, and job URL
* Stores scraped data in an Excel file
* Compares newly scraped jobs with existing records
* Adds only new jobs
* Prevents duplicate job entries using the Job URL
* Preserves previously collected jobs
* Handles missing or unavailable job information
* Maintains a log file for scraper activity and errors
* Displays scraping progress in the terminal

---

## 3. Technologies Used

* **Python 3.10+**
* **Playwright** – Browser automation and web scraping
* **Pandas** – Data processing
* **OpenPyXL** – Excel file handling
* **Microsoft Excel / WPS Office** – Viewing the output

---

## 4. Project Structure

```text
naukri-job-scraper/
│
├── naukri_scraper.py       # Main scraper program
├── naukri_jobs.xlsx        # Existing Excel output
├── requirements.txt        # Required Python packages
├── README.md               # Project documentation
├── scraper.log             # Scraper activity and error logs
└── .gitignore              # Git ignored files
```

> The `venv` folder is not included in the GitHub repository. It should be created locally during setup.

---

# 5. Installation / Setup

Follow the steps below to run the project on a Windows computer.

## Step 1: Install Python

Install **Python 3.10 or newer**.

Check whether Python is installed:

```bash
python --version
```

Example:

```text
Python 3.10.x
```

---

## Step 2: Download the Project

Download or clone this GitHub repository to your computer.

After downloading the ZIP file, extract it.

Open the extracted project folder.

The folder should contain:

```text
naukri_scraper.py
naukri_jobs.xlsx
requirements.txt
README.md
scraper.log
.gitignore
```

---

## Step 3: Open Command Prompt in the Project Folder

Open Command Prompt or PowerShell.

Navigate to the project folder.

Example:

```bash
cd Desktop\naukri-job-scraper
```

Make sure you are inside the folder containing `naukri_scraper.py`.

You can check using:

```bash
dir
```

---

## Step 4: Create a Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

This creates a local `venv` folder for the project dependencies.

---

## Step 5: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

After activation, the terminal should show:

```text
(venv)
```

Example:

```text
(venv) C:\Users\User\Desktop\naukri-job-scraper>
```

---

## Step 6: Install Required Packages

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This installs the libraries required by the project.

---

## Step 7: Install Playwright Chromium Browser

Install the Chromium browser required by Playwright:

```bash
playwright install chromium
```

Wait until the installation is completed successfully.

---

# 6. How to Run the Scraper

After completing the installation, run:

```bash
python naukri_scraper.py
```

The complete process is:

### 1. Open the project folder

```bash
cd Desktop\naukri-job-scraper
```

### 2. Activate the virtual environment

```bash
venv\Scripts\activate
```

### 3. Run the scraper

```bash
python naukri_scraper.py
```

### 4. The scraper will:

* Open Naukri.com using Playwright
* Search for Python Developer jobs
* Find available job listings
* Extract the required job details
* Compare them with the existing Excel records
* Skip duplicate jobs
* Add only new jobs
* Save the updated data to the Excel file
* Record execution details in the log file

### Example Output

```text
Opening Naukri...
Page loaded successfully.
Page title: Python Developer Jobs - Naukri.com
Job cards found: 20

Scraped job 1: Python Developer
Scraped job 2: Python Software Developer
...

Saving jobs to Excel...
Existing jobs in Excel: 40
No new jobs found.

Scraping completed successfully.
```

---

# 7. Excel Output

The scraped data is stored in:

```text
naukri_jobs.xlsx
```

The Excel file contains information such as:

| Column      | Description                         |
| ----------- | ----------------------------------- |
| Job Title   | Name of the job                     |
| Company     | Company offering the job            |
| Location    | Job location                        |
| Experience  | Required experience                 |
| Skills      | Skills mentioned in the job listing |
| Posted Date | Job posting date                    |
| Job URL     | URL of the job listing              |

After running the scraper, open `naukri_jobs.xlsx` using Microsoft Excel or WPS Office to view the results.

---

# 8. Duplicate / New-Job Handling

The scraper compares newly scraped jobs with the existing records in `naukri_jobs.xlsx`.

The **Job URL** is used to identify unique job listings.

### If the job already exists

The scraper skips the job and does not create another duplicate entry.

Example:

```text
Existing jobs in Excel: 40
No new jobs found.
```

### If a new job is found

The scraper adds the new job to the existing Excel file.

Previously collected jobs are preserved.

This allows the Excel file to maintain previously collected job listings while adding only newly discovered jobs.

---

# 9. Logging / Error Handling

The scraper maintains a log file:

```text
scraper.log
```

The log records important information such as:

* Scraper execution
* Page loading
* Job scraping activity
* Excel operations
* Errors and exceptions
* Completion status

If an error occurs during execution, check `scraper.log` for details.

---

# Complete Setup and Run Process

For a new user, follow these commands in order:

### 1. Go to the project folder

```bash
cd Desktop\naukri-job-scraper
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright browser

```bash
playwright install chromium
```

### 6. Run the scraper

```bash
python naukri_scraper.py
```

### 7. Check the output

Open:

```text
naukri_jobs.xlsx
```

### 8. Check logs if required

Open:

```text
scraper.log
```

---

## Project Deliverables

The repository contains:

* `naukri_scraper.py` – Main Python scraper
* `naukri_jobs.xlsx` – Excel output
* `requirements.txt` – Required dependencies
* `README.md` – Project documentation
* `scraper.log` – Execution log
* `.gitignore` – Git configuration
