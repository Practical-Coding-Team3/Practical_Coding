from fastapi import APIRouter, Request
from server.routers.text_correction import text_correction

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    core_word = text_correction(text)
    return {"received_text": text, "core_word": core_word}