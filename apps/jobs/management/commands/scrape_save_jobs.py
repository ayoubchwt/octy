import asyncio 
from django.core.management.base import BaseCommand
from infrastructure.scraper.run_scrapers import scrape_all
from apps.jobs.services import JobService
class Command(BaseCommand) : 
    help = "Run the scraper pipeline and save cleaned jobs to database." 
    def handle(self, *args , **options) : 
        cleaned_jobs = asyncio.run(scrape_all())
        JobService.job_batch_create(scraped_jobs = cleaned_jobs)
