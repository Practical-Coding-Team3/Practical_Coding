from fastapi import APIRouter, Request
from server.routers.keyword_extraction import keyword_extraction, get_category_and_related_info
from server.routers.api import related_url

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word = keyword_extraction(text)
    related_word = get_category_and_related_info(core_word)
    url = related_url(text, related_word)

    return {"received_text": text, "core_word": core_word, "related_word": related_word, "url": url}