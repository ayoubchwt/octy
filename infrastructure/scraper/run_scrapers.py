from infrastructure.scraper.sources.arbeitnow import fetchArbeitJobs
from infrastructure.scraper.sources.nomado import fetchNomadoJobs
from infrastructure.scraper.sources.nofluffjobs import fetchNofluffjobs
from infrastructure.scraper.schemas.job import Job
from infrastructure.scraper.clean_result import job_clean_normalize
import asyncio
import json
async def scrape_all() : 
    results = await asyncio.gather(
        asyncio.to_thread(fetchArbeitJobs,jobs_number = 10),                                                                                                                                          
        asyncio.to_thread(fetchNomadoJobs,jobs_number = 10),    
        fetchNofluffjobs(jobs_number = 10),
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

jobs = asyncio.run(scrape_all())
for item in jobs:
    print(item)