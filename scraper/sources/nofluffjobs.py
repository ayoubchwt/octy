from dotenv import load_dotenv
import os
import asyncio
from camoufox.async_api import AsyncCamoufox
async def collect_jobs_data(href : str) :
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=True) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL + href)
            print(f"{response.status} {await page.title()}")
    except Exception as e : 
        print(e)
    
async def collect_jobs_href() : 
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=True) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL)
            if not response.status == 200 : 
                raise ConnectionError(f"Connection with NoFluffJobs got rejceted - status code :{response.status}")
            cards = page.locator('[id^="nfjPostingListItem-"]')
            hrefs : list[str] = [] 
            for i in range(await cards.count()) : 
                card = cards.nth(i)
                href = await card.get_attribute("href")
                await collect_jobs_data(href)
    except Exception as e : 
        print(e)
asyncio.run(collect_jobs_href())
