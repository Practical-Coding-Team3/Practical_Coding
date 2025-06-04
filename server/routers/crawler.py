from typing import Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.utils.crawler import crawl_url

router = APIRouter(prefix="/crawl", tags=["crawler"])


class CrawlRequest(BaseModel):
    url: str  # 크롤링할 웹페이지 URL


class CrawlResponse(BaseModel):
    metadata: Dict[str, str]      # HTML 메타태그 정보
    content: str                  # 추출된 본문 텍스트
    image_url: Optional[str]      # 대표 이미지 URL (없을 수도 있음)


@router.post("", response_model=CrawlResponse)
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
