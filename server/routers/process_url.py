from typing import Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.utils.process import process_url 

router = APIRouter(prefix="/process", tags=["processor"])

class URLRequest(BaseModel):
    url: str                      # 요약할 기사 URL
    is_first: Optional[bool] = False  # 첫 번째 기사일 경우 상세 요약 적용


class URLResponse(BaseModel):
    url: str
    metadata: Dict[str, str]
    summary: str
    image_url: Optional[str]


@router.post("", response_model=URLResponse)
def process_url_api(request: URLRequest):
    """
    URL을 받아서 크롤링하고 요약까지 한 번에 처리

    - is_first=True일 경우 첫 기사라서 상세 요약 사용
    - 그 외는 간단 요약 사용
    """
    try:
        result = process_url(request.url, is_first=request.is_first)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
