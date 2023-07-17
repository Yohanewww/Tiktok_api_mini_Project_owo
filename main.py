from fastapi import FastAPI, Request
from pydantic import BaseModel
app = FastAPI()
from main_scraper import Scraper
from fastapi.responses import ORJSONResponse, FileResponse
api = Scraper()
import urllib.request
import json
import base64

import uvicorn

class API_Hybrid_Response(BaseModel):
    status: str = None
    message: str = None
    endpoint: str = None
    url: str = None
    type: str = None
    platform: str = None
    aweme_id: str = None
    total_time: float = None
    official_api_url: dict = None
    desc: str = None
    create_time: int = None
    author: dict = None
    music: dict = None
    statistics: dict = None
    cover_data: dict = None
    hashtags: list = None
    video_data: dict = None
    image_data: dict = None

@app.get("/")
async def root():
    return {"message": "Hello Wxorld"}


@app.get("/scrape/{encoded}",  response_model=API_Hybrid_Response)
async def scrape_video_data(encoded) :
    decoded = base64.b64decode(encoded).decode("utf-8")
    data = await api.link_parse(decoded)    
    return ORJSONResponse(data)

