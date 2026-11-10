import os
from dotenv import load_dotenv
import requests
from infrastructure.scraper.schemas.job import Job
from bs4 import BeautifulSoup
from datetime import datetime,timezone
import time
def fetchArbeitJobs(page : int = 4, jobs_number = 1000) -> list[Job]:
    print("scraping Arbeitnow ...")
    load_dotenv()
    API_URL= os.getenv("NOMADO_API")
    if not API_URL : 
        raise ValueError("NOMADO_API is missing from .env")
    jobs : list[Job] = []
    while True :
        response = requests.get(
            API_URL,
            params={"page" : page},
            timeout=20
            )
        if response.status_code == 429 : 
            print("Rate limited. Waiting 30 seconds...")
            time.sleep(30)
            continue
        response.raise_for_status()
        data = response.json().get("data",[])
        if not data : 
            print("No more jobs found")
            break
        for item in data : 
            desciption = BeautifulSoup(
                item.get("description",""),
                "html.parser",
            ).get_text(" ",strip=True)
            job : Job = {
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("location", ""),
                "language" : item.get("language", ""),
                "country": "Germany",
                "description": desciption,
                "url": item.get("url", ""),

                "employment_type": "unknown",

                "salary_min": None,
                "salary_max": None,
                "salary_currency": None,
                "salary_period": None,

                "skills": item.get("tags", []),
                "source": "arbeitnow",
                "source_job_id": str(item.get("slug", "")) or None,

                "posted_at": item.get("created_at"),
                "first_seen_at": datetime.now(timezone.utc).isoformat(),
            }
            jobs.append(job)
        page+=1
        if len(jobs) >= jobs_number : 
            break
    print(f"{len(jobs)} jobs scraped from Arbeitnow successfully")
    return jobs