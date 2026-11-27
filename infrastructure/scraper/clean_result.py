from infrastructure.scraper.schemas.job import Job
import pandas as pd
import numpy as np
def job_clean_normalize(jobs : list[Job] = []) -> list[Job] : 
    # clean, normalize and validate scraped jobs
    if not jobs : 
        print("Job list is empty")
        return jobs
    df = pd.DataFrame(jobs)
    df = df.dropna(subset=["title" , "title" , "company", "source_job_id", "source" , "url"])
    unknown_cols = ["location", "country","employment_type" , "language" , "description", "salary_period"]
    for col in unknown_cols :   
        if col in df.columns : 
            df[col] = df[col].fillna("unknown").astype(str).str.strip()
            df[col] = df[col].replace("","unknown")
        else : 
            print(f"{col} does not exist in the dataframe")

    numeric_cols = ["salary_max","salary_min"]
    for col in numeric_cols : 
        if col in df.columns : 
            df[col] = pd.to_numeric(df[col],errors="coerce")
            df[col] = df[col].replace({np.nan : None})
        else :     
            print(f"{col} does not exist in the dataframe")
    if "skills" in df.columns : 
        df["skills"] = df["skills"].apply(
            lambda x : x if isinstance(x, list) else []
        )
    else :
        print("skill does not exist in the dataframe")
    
    date_columns = ["posted_at" , "first_seen_at"]
    for col in date_columns : 
        if col in df.columns : 
            df[col] = pd.to_datetime(df[col] , errors="coerce")
            df[col] = df[col].replace({np.nan : None})
        else : 
            print(f"{col} does not exist in the dataframe")    
    df = df.drop_duplicates(subset=["url", "source_job_id"],keep="last")
    dict_list = df.to_dict(orient="records")
    return dict_list