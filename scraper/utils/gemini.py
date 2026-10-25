import os
from dotenv import load_dotenv
from google import genai

def clean_description(description : str = "") :
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY : 
        raise ValueError("GEMINI_API_KEY is missing from .env")
    if not description.strip() :
        return ""
    try : 
        client = genai.Client(api_key=GEMINI_API_KEY)
        interactions = client.interactions.create(
            model="gemma-4-26b-a4b-it",
            input=f"""
                Rewrite the following job description into clean, readable text.
                Rules:
                - Preserve all important job requirements and responsibilities.
                - Remove HTML leftovers and redundant formatting.
                - Do not invent or assume information.
                - Return only the cleaned description.
                Job description:
                {description}
            """,
            )
        return interactions.output_text
    except Exception as e : 
        print(e)    