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
    core_word, action_word = keyword_extraction(text)
    category, related_word = get_category_and_related_info(core_word)

    if category == "해당 없음":
        category = not_found_category(core_word)
        related_word = get_related_info(category)

    if not related_word:
        related_word = not_found_related_word(category)

    raw_url = related_url(core_word, related_word, action_word)

    urls = re.findall(r'https?://[^\s\])]+', raw_url)

    main_url = ""
    sub_url = ""
    for i in range(len(urls)):
        if i ==0:
            main_url = urls[i]
        elif i == 1:
            sub_url = urls[i]
        elif i % (1 + len(related_word)) == 0:
            main_url = main_url + " | " + urls[i]
        else:
            sub_url = sub_url + " | " + urls[i]


    return {"received_text": text, "core_word": core_word, "main": main_url, "sub": sub_url}