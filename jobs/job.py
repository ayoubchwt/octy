from django.db import models

class Job(models.Model) : 
    
    id = models.AutoField()
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_lenght=200)
    
    location = models.CharField(max_lenght=200)
    country = models.CharField(max_length=200)
    
    employment_type = models.CharField(max_length=30, default="unknown")
    workplace_type = models.CharField(max_length=30, default="unknown")
    experience_level = models.CharField(max_lenght = 30 ,default="unknown")
    
    
    salary_min = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    
    salary_max = models.DecimalField(
        max_degits=12, decimal_places=2, null=True, blank=True 
    )
    
    salary_currency = models.CharField(max_length=10)
    salary_period = models.CharField(max_length=10)
    
    skills = models.JSONField(default=list, blank=True)
    
    source = models.CharField(max_length=100, blank=True, null=True)
    source_job_id = models.CharField(max_length=200, blank=True, null=True)
    url = models.URLField(unique=True)
    
    posted_at = models.DateTimeField(null=True, blank=True)
    first_seen_at = models.DateTimeField(null=True, blank=True)
    
    def __init__(self):
        pass
    
    
    
    