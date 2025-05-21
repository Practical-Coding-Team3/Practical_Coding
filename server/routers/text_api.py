from fastapi import APIRouter, Request
from server.routers.text_correction import text_correction, get_category_and_related_info
from server.routers.api import related_url

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word = text_correction(text)
    category, related_word = get_category_and_related_info(core_word)
    related_word = get_category_and_related_info(core_word)

    return {"received_text": text, "core_word": core_word}