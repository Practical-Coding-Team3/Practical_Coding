from fastapi import APIRouter, Request, HTTPException
from utils.crawler import crawl_url
from utils.summarizer import summarize_text_first, summarize_text_remain

from pydantic import BaseModel
from typing import Dict, Optional


router = APIRouter(prefix="/summary", tags=["summary"])

#  1. URL 크롤링 API (/crawl)
class CrawlRequest(BaseModel):
    url: str  # 크롤링할 웹페이지 URL

# 응답 모델: API가 반환할 데이터 구조
class CrawlResponse(BaseModel):
    metadata: Dict[str, str]      # HTML 메타태그 정보
    content: str                  # 추출된 본문 텍스트
    image_url: Optional[str]      # 대표 이미지 URL (없을 수도 있음)

@router.post("/crawl", response_model=CrawlResponse)
def crawl_endpoint(request: CrawlRequest):
    """
    주어진 URL을 크롤링하여 본문, 메타데이터, 대표 이미지를 추출
    """
    try:
        metadata, content, image_url = crawl_url(request.url)
        return {
            "metadata": metadata,
            "content": content,
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. 텍스트 요약 API (/summarize)
class SummarizeRequest(BaseModel):
    text: str                 # 요약 대상 본문 텍스트
    detail: Optional[bool] = False  # True면 자세히, False면 3줄 요약

# 응답 모델
class SummarizeResponse(BaseModel):
    summary: str  # 생성된 요약 결과

@router.post("/summarize", response_model=SummarizeResponse)
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

# 3. 통합 처리 API (/process_url)
class URLRequest(BaseModel):
    url: str                     # 요약할 기사 URL
    is_first: Optional[bool] = False  # 첫 번째 기사일 경우 상세 요약 적용

# 응답 모델: 전체 요약 결과
class URLResponse(BaseModel):
    url: str
    metadata: Dict[str, str]
    summary: str
    image_url: Optional[str]

@router.post("/process_url", response_model=URLResponse)
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