from infrastructure.scraper.sources.arbeitnow import fetchArbeitJobs
from infrastructure.scraper.sources.nomado import fetchNomadoJobs
from infrastructure.scraper.sources.nofluffjobs import fetchNofluffjobs
from infrastructure.scraper.schemas.job import Job
from infrastructure.scraper.clean_result import job_clean_normalize
import asyncio
import json
import os
from dotenv import load_dotenv
async def scrape_all() : 
    load_dotenv()
    JOB_NUMBER_PER_SCRAPER = int(os.getenv("JOB_NUMBER_PER_SCRAPER")) | 10
    results = await asyncio.gather(
        asyncio.to_thread(fetchArbeitJobs,jobs_number = JOB_NUMBER_PER_SCRAPER),                                                                                                                                          
        asyncio.to_thread(fetchNomadoJobs,jobs_number = JOB_NUMBER_PER_SCRAPER),    
        fetchNofluffjobs(jobs_number = JOB_NUMBER_PER_SCRAPER),
        return_exceptions=True
    )
    jobs : list[Job] = []
    for result in results : 
        if isinstance(result, Exception):
            print(f"Scraper failed with error: {result}")
        elif isinstance(result, list):
            jobs.extend(result)
    with open("exported_mock_data.json","w",encoding="utf-8") as file :
        json.dump(jobs,file,indent=4)
    
    cleaned_jobs = job_clean_normalize(jobs)
    return cleaned_jobs