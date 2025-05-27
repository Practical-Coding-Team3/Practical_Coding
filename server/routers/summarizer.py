from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.utils.summarizer import summarize_text_first, summarize_text_remain

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str                      # 요약 대상 본문 텍스트
    detail: Optional[bool] = False  # True면 자세히, False면 간단 요약


class SummarizeResponse(BaseModel):
    summary: str  # 생성된 요약 결과


@router.post("", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest):
    """
    주어진 본문 텍스트를 Gemini API를 이용해 요약
    detail = True → 긴 기사 요약 (문단 기반)
    detail = False → 헤드라인 3줄 요약
    """
    try:
        if request.detail:
            summary = summarize_text_first(request.text)
        else:
            summary = summarize_text_remain(request.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
