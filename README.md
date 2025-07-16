# 🕸️ JobPaw Web Scraping

This repository contains a small set of scripts used to scrape job postings from the [JobPaw](https://www.jobpaw.com/) website. The goal is to collect links to job listings and then retrieve the details for each listing in order to analyse them offline.

---

## 📂 Repository Contents

- 🧲 `getLinksScript.py` – retrieves all job posting links and writes them to `jobPawLinks.xlsx`.
- 📄 `getJobDetailsScript.py` – downloads the details for each link found in the previous step and saves them in `jobDetails.xlsx`.
- 📓 Jupyter notebooks (`getLinks-nb.ipynb`, `getJobDetails-nb.ipynb`, `dataProcessing-nb.ipynb`) mirror the scripts for interactive use.

🔍 The resulting Excel files can then be processed to perform data analysis or further NLP tasks.

---

## 🧱 Project Structure

```
├── getLinksScript.py           # scrapes job posting URLs
├── getJobDetailsScript.py      # downloads each job description
├── getLinks-nb.ipynb           # notebook form of the link scraper
├── getJobDetails-nb.ipynb      # notebook form of the details scraper
├── dataProcessing-nb.ipynb     # notebook for analysing the Excel outputs
├── docs/                       # documentation and helper scripts
│ └── test.py                   # simple test used during development
├── jobPawLinks.xlsx            # results from getLinksScript.py
├── jobDetails.xlsx             # results from getJobDetailsScript.py
├── pycache/                    # bytecode cache created by Python
├── .vscode/                    # editor configuration files
├── .idea/                      # IDE project files
├── .gitattributes              # repository text/binary settings
├── .DS_Store                   # macOS metadata file (can be ignored)
└── README.md                   # project documentation
```

---

## ⚙️ Requirements

The scripts require **Python 3** and the following packages:

```
requests
beautifulsoup4
pandas
openpyxl                        # required by pandas for Excel output
```

📦 Install them via:

```bash
pip install -r requirements.txt
```

# ▶️ Usage

- 🔗 Run python getLinksScript.py to create jobPawLinks.xlsx containing all job links.

- 📑 Run python getJobDetailsScript.py to fetch each job description from the previously generated links file. The results will be stored in jobDetails.xlsx.

💡 Both scripts display a progress bar while running and may pause periodically to avoid overwhelming the JobPaw servers.

# ⚠️ Disclaimer

These scripts are provided for educational purposes.
When scraping any website, ensure that you respect its terms of service and local laws. Excessive or automated access to web content may lead to your IP being blocked.
