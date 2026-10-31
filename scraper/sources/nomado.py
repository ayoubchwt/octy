from dotenv import load_dotenv
from scraper.schemas.job import Job
import os
import requests
import pandas as pd
from datetime import timezone, datetime

def fetchNomadoJobs(page : int = 1) -> list[Job] : 
    load_dotenv()
    API_URL= os.getenv("NOMADO_API")
    if not API_URL : 
        raise ValueError("NOMADO_API is missing from .env")
    try : 
        response = requests.get(
            API_URL,
            params={"page" : page},
            timeout=20,
            )
        response.raise_for_status()
        data = response.json().get("data",[])     
        jobs : list[Job] = []   
        for item in data : 
            job : Job = {
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("location", ""),
                "language" : item.get("language" ,""),
                "country": "Germany",
                "description": "",
                "url": item.get("url", ""),

                "employment_type": "unknown",

                "salary_min": item.get("salaryMin"),
                "salary_max": item.get("salaryMax"),
                "salary_currency": item.get("currency"),
                "salary_period": "month",

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
     