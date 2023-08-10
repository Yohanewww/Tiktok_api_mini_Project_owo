"FASTAPI MAIN FILE"
from typing import Annotated
from fastapi import FastAPI, Path
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
import uvicorn
import pyfiglet
from tiktok_scraper import Scraper

TITLE= "Tiktok_api_mini_Project_owo"
SUMMARY="Deadpool's favorite app. Nuff said."
DESCRIPTION = """
#### Description/说明
<details>
<summary>点击展开/Click to expand</summary>
> [中文/Chinese]
- 爬取抖音和TikTok的数据并返回。更多功能正在开发中。
- 此項目是為了讓我學習如何開發Api而開發的，如果你有什麼建議或者想法，歡迎聯繫我。
- 此項目的參考來自[https://github.com/Evil0cta
l/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API)
- 本项目仅供学习交流使用，严禁用于违法用途，如有侵权请联系作者。
> [英文/English]
- Crawl the data of Douyin and TikTok and return it. More features are under development.
</details>
#### Contact author/联系作者
<details>
<summary>Click to expand/点击展开</summary>
- Discord: yohane_owo
- Email: [yohane910@gmail.com](mailto:yohane910@gmail.com)
- Github: [https://github.com/yohaneowo](https://github.com/yohaneowo)
</details>
"""
VERSION="0.0.1"

tags_metadata = [
    {
        "name": "Hybrid Request (Tiktok&Douyin)",
        "description": "input str with url will do ",
    }
]

api = Scraper()

app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    version=VERSION,
)


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


@app.get("/api/hybrid_parsing/{url:path}",  response_model= API_Hybrid_Response,tags= ['Hybrid Request (Tiktok&Douyin)'])
async def scrape_video_data(url) :
    """
    Args:
        String with Url | Url

    Returns:
        JSON
    """
    url: Annotated[str, Path(title="String with url | Url", description="你好")]
    if url:
        data = await api.link_parse(url)
        return ORJSONResponse(data)

if __name__ == '__main__':
    T = "Tiktok Api owo"
    ASCII_art_1 = pyfiglet.figlet_format(T)
    print(pyfiglet.__file__)
    print(ASCII_art_1)
    uvicorn.run('main:app', host='127.0.0.1', port=4488, reload=True, workers=8)
    
    