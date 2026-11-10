from django.db import models

class Job(models.Model):

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200, blank=True, default="unknown")
    country = models.CharField(max_length=200, blank=True, default="unknown")

    employment_type = models.CharField(max_length=30, default="unknown")
    language = models.CharField(max_length=30, default="unknown")
    description= models.TextField(default="unknown")
    url = models.URLField(unique=True)
    
    salary_min = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    salary_max = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    salary_currency = models.CharField(max_length=10, blank=True, default="")
    salary_period = models.CharField(max_length=10, blank=True, default="")

    skills = models.JSONField(default=list, blank=True)
    source = models.CharField(max_length=100)
    source_job_id = models.CharField(max_length=100, unique=True)

    posted_at = models.DateTimeField(null=True, blank=True)
    first_seen_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta: 
        ordering = ["-first_seen_at"]
    def __str__(self) : 
        return f"{self.title} at {self.company} from {self.source}"

