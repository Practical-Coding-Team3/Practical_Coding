from fastapi import APIRouter, Request
from utils.crawler import crawl_url
from utils.summarizer import summarize_text_first, summarize_text_remain
from main import process_url

router = APIRouter(prefix="/summary", tags=["summary"])

@router.post("/")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    print(text)
    return {"received_text": text}