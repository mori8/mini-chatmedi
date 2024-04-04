from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()


class Query(BaseModel):
    prompt: str

@app.post("/generate-text/")
async def generate_text(query: Query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": query.prompt},
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
