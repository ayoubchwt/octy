from dotenv import load_dotenv
from scraper.schemas.job import Job
import os
import requests
def fetchNomadoJobs(page : int = 1) -> list[Job] : 
    load_dotenv()
    API_URL= os.getenv("NOMADO_API")
    if not API_URL : 
        raise ValueError("NOMADO_API is missing from .env")
    try : 
        response = requests.get(
            API_URL,
            params={"page" : page},
            timeout=20,
            )
        response.raise_for_status()
        data = response.json().get("data",[])
        print(data)
        
    except Exception as e : 
        print(e)
    
fetchNomadoJobs()
     