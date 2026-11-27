from django.db import transaction
from infrastructure.scraper.schemas.job import Job as ScrapedJob
from .models import Job

class JobService : 
    
    @staticmethod
    def job_create_or_update(*, job : dict[str,any]) -> tuple[Job ,bool] : 
        url = job["url"]
        defaults = job.copy()
        defaults.pop("url", None)
        return Job.objects.update_or_create(
            url=url, 
            defaults=defaults
        )
    @classmethod 
    @transaction.atomic()
    def job_batch_create(cls, *, scraped_jobs : list[dict[str,any]]) -> None : 
        created_count = 0 
        updated_count = 0
        for job in scraped_jobs : 
            try : 
                _, created = JobService.job_create_or_update(job = job)
                if created :
                    created_count += 1 
                else : 
                    updated_count += 1 
            except Exception as e :
                print(f"Error saving {job.get('source_job_id')} ({job.get('url')}): {e}") 
                
        print(f"Insert Job operations done: {created_count} created, {updated_count} updated.")    


