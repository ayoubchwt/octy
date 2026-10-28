from typing import _TypedDict 
class Job(_TypedDict) :
    title: str
    company: str
    location: str
    language : str
    country: str
    description: str
    url: str
    
    employment_type: str
    workplace_type: str
    experience_level: str
    
    salary_min: float | None
    salary_max: float | None
    salary_currency: str | None
    salary_period: str | None
    
    skills: list[str]
    source: str
    source_job_id: str | None
    
    posted_at: str | None
    first_seen_at: str | None
    