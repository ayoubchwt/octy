from django.db import transaction
from infrastructure.scraper.schemas.job import Job as ScrapedJob
from models import Job

class JobService : 
    
    @staticmethod
    @transaction.atomic()
    def jobs_create_or_update(*, scraped : ScrapedJob) -> tuple[Job ,bool] : 
        # insert a single scraped job into db
        return Job.objects.update_or_create(scraped)

