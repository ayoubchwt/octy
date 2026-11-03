from dotenv import load_dotenv
import os
import re
import asyncio
from camoufox.async_api import AsyncCamoufox
from scraper.schemas.job import Job
from datetime import datetime, timezone

def _parse_salary(salary_text: str | None) -> tuple[float | None, float | None, str | None, str | None]:
    
    if not salary_text:
        return None, None, None, None

    cleaned = salary_text.replace("\xa0", " ")
    lower = cleaned.lower()

    if "month" in lower:
        period = "month"
    elif "day" in lower:
        period = "day"
    elif "hour" in lower:
        period = "hour"
    elif "year" in lower:
        period = "year"
    else:
        period = None

    currency = "PLN"
 
    parts = re.split(r"\s*[-–—]\s*", cleaned)
    numbers: list[float] = []
    for part in parts:
        digits_only = re.sub(r"[^\d.,]", "", part).replace(",", ".")
        if digits_only:
            try:
                numbers.append(float(digits_only))
            except ValueError:
                continue

    if len(numbers) >= 2:
        return numbers[0], numbers[1], currency, period
    elif len(numbers) == 1:
        return numbers[0], numbers[0], currency, period
    return None, None, currency, period

async def collect_jobs_data(href: str, page) -> Job:
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL:
        raise ValueError("NO_FLUFF_JOBS_URL is missing from .env")

    target_url = NO_FLUFF_JOBS_URL.rstrip("/") + "/" + href.lstrip("/")

    try:
        response = await page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
        if response is None or response.status > 400:
            status_code = response.status if response else "No response"
            raise ConnectionError(f"Connection with NoFluffJobs details page got rejected - status code: {status_code}")
        
        title_loc = page.locator('div[class*="posting-details-description"] h1')
        title = (await title_loc.first.inner_text()).strip() if await title_loc.count() > 0 else ""

        company_loc = page.locator('#postingCompanyUrl')
        company = (await company_loc.first.inner_text()).strip() if await company_loc.count() > 0 else ""

        loc_elem = page.locator('span[class*="locations-text"] span')
        location = (await loc_elem.first.inner_text()).strip() if await loc_elem.count() > 0 else ""

        desc_loc = page.locator('#posting-description')
        description = (await desc_loc.first.inner_text()).strip() if await desc_loc.count() > 0 else ""

        req_loc = page.locator('#posting-requirements li span, [commonpostingitemtag]')
        skills = [s.strip() for s in await req_loc.all_inner_texts() if s.strip()]

        salary_loc = page.locator('div[class*="salary "]')
        salary_text = (await salary_loc.first.inner_text()).strip() if await salary_loc.count() > 0 else ""
        salary_min, salary_max, salary_currency, salary_period = _parse_salary(salary_text)

        job_nature_indicator = await page.locator(".common-posting-locations").count()

        language_detect_source = f"{title} {' '.join(skills)} {description}".lower()
        language = "english" if "english" in language_detect_source else "polish"

        now_iso = datetime.now(timezone.utc).isoformat()

        job_data: Job = {
            "title": title,
            "company": company,
            "location": location,
            "language": language,
            "country": "Poland",
            "description": description,
            "url": target_url,
            "employment_type": "hybrid" if job_nature_indicator > 0 else "remote",
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_currency": salary_currency or "PLN",
            "salary_period": salary_period,
            "skills": skills,
            "source": "nofluffjobs",
            "source_job_id": href,
            "posted_at": now_iso,
            "first_seen_at": now_iso,
        }
        return job_data
    except Exception as e:
        print(f"Error fetching job details for {href}: {e}")
        raise
async def _close_notification(page) -> None:
    notification_dialogue = page.locator('div[class="cdk-overlay-container"]')
    try : 
        await notification_dialogue.wait_for(
            state="visible",
            timout=30000 
        )
        print("notification dialogue", notification_dialogue.count())
        if await notification_dialogue.count() > 0:
            viewport = page.viewport_size or {"width": 1280, "height": 720}
            
            x = viewport["width"] / 2
            y = viewport["height"] / 2
            
            await page.mouse.click(x, y)
    except Exception : 
        print("Notification dialogue did not appear.")

async def _show_more_jobs(page, target_count: int = 200) -> None:
    while True:
        card_count = await page.locator('[id^="nfjPostingListItem-"]').count()
        if card_count >= target_count:
            break
        button = page.get_by_role("button", name="See more offers")
        if not await button.is_visible():
            try:
                await button.wait_for(state="visible", timeout=6000)
            except Exception:
                break
            
        await button.click()
        try:
            await page.wait_for_function(
                """(prevCount) => document.querySelectorAll('[id^="nfjPostingListItem-"]').length > prevCount""",
                arg=card_count,
                timeout=8000,
            )
        except Exception:
            await asyncio.sleep(1.0)
            
async def collect_jobs() -> list[Job]:
    load_dotenv()
    NO_FLUFF_JOBS_URL = os.getenv("NO_FLUFF_JOBS_URL")
    if not NO_FLUFF_JOBS_URL:
        raise ValueError("NO_FLUFF_JOBS_URL is missing from .env")
    try:
        async with AsyncCamoufox(headless=False) as browser:
            page = await browser.new_page()
            response = await page.goto(NO_FLUFF_JOBS_URL, wait_until="domcontentloaded")
            if response is None or response.status > 400:
                status_code = response.status if response else "No response"
                raise ConnectionError(f"Connection with NoFluffJobs got rejected - status code: {status_code}")
            await _close_notification(page)
            await _show_more_jobs(page, 700)
            card_elements = await page.locator('[id^="nfjPostingListItem-"]').all()
            print(len(card_elements))
            hrefs: list[str] = []
            for card in card_elements:
                href = await card.get_attribute("href")
                if href:
                    hrefs.append(href)

            jobs: list[Job] = []
            for href in hrefs:
                job = await collect_jobs_data(href, page)
                jobs.append(job)
                await asyncio.sleep(1.0)
            return jobs
    except Exception as e:
        print(e)
        raise

result = asyncio.run(collect_jobs())
print(len(result))