from fastapi import APIRouter, Request
from server.utils.keyword_extraction import keyword_extraction, get_category_and_related_info, not_found_category, not_found_related_word, get_related_info
from server.routers.api import related_url
import json
import httpx
import re

import httpx

async def is_valid_url(url):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.head(url)
            return response.status_code < 400
    except Exception:
        return False
router = APIRouter(prefix="/text", tags=["text"])
@router.post("/core_word")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word, action_word = keyword_extraction(text)
    category, related_word = get_category_and_related_info(core_word)

    if category == "해당 없음":
        category = not_found_category(core_word)
        related_word = get_related_info(category)

    if not related_word:
        related_word = not_found_related_word(category)

    raw_url = related_url(core_word, related_word, action_word)

    urls = re.findall(r'https?://[^\s\])]+', raw_url)

    valid_urls = []
    for url in urls:
        if await is_valid_url(url):
            valid_urls.append(url)

    main_url = ""
    sub_url = ""
    for i in range(len(valid_urls)):
        if i == 0:
            main_url = valid_urls[i]
        elif i == 1:
            sub_url = valid_urls[i]
        elif i % (1 + len(related_word)) == 0:
            main_url = main_url + " | " + valid_urls[i]
        else:
            sub_url = sub_url + " | " + valid_urls[i]


    return {"received_text": text, "core_word": core_word, "main": main_url, "sub": sub_url}