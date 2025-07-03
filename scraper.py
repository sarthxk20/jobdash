import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_remoteok_jobs():
    url = "https://remoteok.com/remote-dev+python-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    job_rows = soup.find_all("tr", class_="job")

    job_titles = []
    companies = []
    locations = []

    for job in job_rows:
        title_tag = job.find("h2", itemprop="title")
        company_tag = job.find("h3", itemprop="name")
        location_tag = job.find("div", class_="location")

        if title_tag and company_tag:
            job_titles.append(title_tag.text.strip())
            companies.append(company_tag.text.strip())
            locations.append(location_tag.text.strip() if location_tag else "Remote")

    if job_titles:
        df = pd.DataFrame({
            "Job Title": job_titles,
            "Company": companies,
            "Location": locations
        })
        df.to_csv("jobs.csv", index=False)
        print(f"✅ Scraped {len(df)} jobs and saved to jobs.csv")
    else:
        print("⚠️ No jobs found. Structure may have changed.")

if __name__ == "__main__":
    scrape_remoteok_jobs()
