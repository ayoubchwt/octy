from dotenv import load_dotenv
import os
import asyncio
from camoufox.async_api import AsyncCamoufox
async def collect_main_cards() : 
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL : 
        raise ValueError("NO_FLUFF_JOBS_UR is missing from .env")
    try : 
        async with AsyncCamoufox(headless=True) as browser : 
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL,wait_until="domcontentloaded")
            print(response.status)
            print(await page.title())
            await browser.close()
    except Exception as e : 
        print(e)
asyncio.run(collect_main_cards())
