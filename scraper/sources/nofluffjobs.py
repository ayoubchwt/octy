from dotenv import load_dotenv
import os
import asyncio
from camoufox.async_api import AsyncCamoufox
from scraper.schemas.job import Job
from datetime import datetime, timezone
async def collect_jobs_data(href : str , page : AsyncCamoufox) -> Job :
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        response = await page.goto(NO_FLUFF_JOBS_URL + href)
        if not response.status == 200 or response is None:
            raise ConnectionError(f"Connection with NoFluffJobs details page got rejceted - status code :{response.status}")
        print(await page.title())
        job_nature_indicator = await page.locator(".common-posting-locations").count()
        print(job_nature_indicator)
        salary_range = (await page.locator('div[class^="salary "]').locator("h4").inner_text()).strip().replace("PLN", "").split()
        salary_period = await page.locator('div[class^="salary "]').inner_text().lower()
        requirements = await page.locator('#posting-requirements li span').inner_text()
        
        return {
            "title" : await page.locator('div[class^="posting-details-description"]').locator("h1").inner_text(),
            "company" : await page.locator('[id="postingCompanyUrl"]').inner_text(),
            "location" : await page.locator('span[class$="locations-text"]').locator("span").inner_text(),
            "language" : "english" if "english" in requirements else "polish",
            "country" : "Poland", 
            "description" : await page.locator('[id="posting-description"]').inner_text(),
            "url" : NO_FLUFF_JOBS_URL + href, 
            "employment_type" : "hybrid" if job_nature_indicator > 0 else "remote",
            "salary_min" : float(salary_range[0]) if len(salary_range) > 0 else "unknown",
            "salary_max" : float(salary_range[1]) if len(salary_range) > 0 else "unknown",
            "salary_currency" : "PLN",
            "salary_period" : "month" if "month" in salary_period else "day" if "day" in salary_period else "hour" if "hour" in salary_period else "unknown", 
            "skills" : requirements,
            "source" : "nofluffjobs", 
            "source_job_id" : href,
            "posted_at" : datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e : 
        print(e)
        raise
    
async def collect_jobs_href() -> list[Job]: 
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=False) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL)
            if not response.status == 200 or response is None: 
                raise ConnectionError(f"Connection with NoFluffJobs got rejceted - status code :{response.status}")
            cards = page.locator('[id^="nfjPostingListItem-"]')
            jobs : list[Job] = []
            for i in range(await cards.count()) : 
                card = cards.nth(i)
                href = await card.get_attribute("href")
                job = await collect_jobs_data(href, page)
                print(job)
                jobs.append(job)
            return jobs
    except Exception as e : 
        print(e)
        raise
result = asyncio.run(collect_jobs_href())
