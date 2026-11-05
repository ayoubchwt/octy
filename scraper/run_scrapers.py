from scraper.sources.arbeitnow import fetchArbeitJobs
from scraper.sources.nomado import fetchNomadoJobs
from scraper.sources.nofluffjobs import fetchNofluffjobs
from scraper.schemas.job import Job
import asyncio

async def scrape_all() : 
    results = await asyncio.gather(
        asyncio.to_thread(fetchArbeitJobs),                                                                                                                                          
        asyncio.to_thread(fetchNomadoJobs),    
        fetchNofluffjobs(),
        return_exceptions=True
    )
    jobs : list[Job] = []
    for result in results : 
        if isinstance(result, Exception):
            print(f"Scraper failed with error: {result}")
        elif isinstance(result, list):
            jobs.extend(result)
    for job in jobs : 
        print(job)

asyncio.run(scrape_all())