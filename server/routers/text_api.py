from fastapi import APIRouter, Request
from server.utils.keyword_extraction import keyword_extraction, get_category_and_related_info, not_found_category, not_found_related_word, get_related_info
from server.routers.api import related_url, add_category
import json

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/core_word")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word = keyword_extraction(text)
    category, related_word = get_category_and_related_info(core_word)
    if category == "해당 없음":
        category = not_found_category(core_word)
        related_word = get_related_info(category) # 관련 단어 검색

    if not related_word: # 관련 단어 없으면 추가 작업 시작
        related_word = not_found_related_word(category)

    keyword = core_word[0]
    url = related_url(keyword, related_word)

    return {"received_text": text, "core_word": core_word, "related_word": related_word, "url": url}