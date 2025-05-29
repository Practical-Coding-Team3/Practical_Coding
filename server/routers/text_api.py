from fastapi import APIRouter, Request
from server.utils.keyword_extraction import keyword_extraction, get_category_and_related_info, not_found_category, not_found_related_word, get_related_info
from server.routers.api import related_url
import json
import re

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/core_word")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word,action_word = keyword_extraction(text)
    category, related_word = get_category_and_related_info(core_word)
    if category == "해당 없음":
        category = not_found_category(core_word)
        related_word = get_related_info(category) # 관련 단어 검색

    if not related_word: # 관련 단어 없으면 추가 작업 시작
        related_word = not_found_related_word(category)


    raw_url = related_url(core_word, related_word, action_word)

    print(raw_url)
    url = {"main": [], "sub": []}

    for word in core_word:
        if word in raw_url:
            main_url = raw_url[word].get(word, "")
            if main_url:
                url["main"].append(main_url)
            # sub: 해당 core_word의 나머지 url들
            sub_urls = [v for k, v in raw_url[word].items() if k != word]
            url["sub"].extend(sub_urls)

    return {"received_text": text, "core_word": core_word, "url": url}