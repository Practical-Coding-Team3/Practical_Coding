from fastapi import APIRouter, Request

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/")
async def receive_text(request: Request):
    data = await request.json()
    text = data.get("text")
    print(text)
    return {"received_text": text}