import os
from dotenv import load_dotenv
import requests
from scraper.schemas.job import Job
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timezone

def fetchArbeitJobs(page : int = 1) -> list[Job]:
    load_dotenv()
    API_URL= os.getenv("NOMADO_API")
    if not API_URL : 
        raise ValueError("NOMADO_API is missing from .env")
    try :
        response = requests.get(
            API_URL,
            params={"page" : page},
            timeout=20
            )
        response.raise_for_status()
        data = response.json().get("data",[])
        jobs : list[Job] = []
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
                "workplace_type": (
                    "remote" if item.get("remote", False) else "unknown"
                ),
                "experience_level": "unknown",

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
        return jobs
    except Exception as e : 
        print(e) 