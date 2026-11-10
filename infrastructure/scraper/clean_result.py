from infrastructure.scraper.schemas.job import Job
import pandas as pd
import json
def job_clean_normalize(jobs : list[Job] = []) -> list[Job] : 
    # clean, normalize and validate scraped jobs
    with open("exported_mock_data.json","r",encoding="utf-8") as file : 
        data = json.load(file)
    if not data : 
        print("Job list is empty")
        return jobs
    df = pd.DataFrame(data)
    print(df)

job_clean_normalize()