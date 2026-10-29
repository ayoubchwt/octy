from dotenv import load_dotenv
import os
import asyncio
from camoufox.async_api import AsyncCamoufox
from scraper.schemas.job import Job
async def collect_jobs_data(href : str) -> Job :
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=False) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL + href)
            if not response.status == 200 :
                raise ConnectionError(f"Connection with NoFluffJobs details page got rejceted - status code :{response.status}")

            description_section, info_section, requirements_section, tasks_section, posting_description_section, posting_specs, salary_section = (
                page.locator('div[class^="posting-details-description"]'),
                page.locator('div[class^="posting-info-row"]'),
                page.locator('[id="posting-requirements"]'),
                page.locator('[id="posting-tasks"]'),
                page.locator('[id="posting-description"]'),
                page.locator('[id="posting-specs"]'),
                page.locator('div[class^="salary "]')
            )
            return {
                "title" : await description_section.locator("h1").inner_text(),
                "company" : await page.locator('[id="postingCompanyUrl"]').inner_text(),
                "location" : await page.locator('span[class=^"locations-text"]').locator("span").inner_text(),
                "language": "English" if "english" in (await requirements_section.locator("li").inner_text()).lower() else "Polish",
                "country" : "Poland", 
                "description" : await posting_description_section.inner_text(),
                "url" : NO_FLUFF_JOBS_URL + href, 
            }
             
    except Exception as e : 
        print(e)
    
async def collect_jobs_href() : 
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=False) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL)
            if not response.status == 200 : 
                raise ConnectionError(f"Connection with NoFluffJobs got rejceted - status code :{response.status}")
            cards = page.locator('[id^="nfjPostingListItem-"]')
            jobs : list[Job] = []
            for i in range(await cards.count()) : 
                card = cards.nth(i)
                href = await card.get_attribute("href")
                job = await collect_jobs_data(href)
                jobs.append(job)
            return jobs
    except Exception as e : 
        print(e)
asyncio.run(collect_jobs_href())
