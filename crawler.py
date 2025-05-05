# import requests
# import re
# from bs4 import BeautifulSoup
# from difflib import SequenceMatcher

# def is_similar(a, b, threshold=0.9):
#     return SequenceMatcher(None, a, b).ratio() > threshold

# def crawl_url(url):
#     """
#     주어진 URL을 크롤링하여 본문에 가까운 텍스트와 대표 이미지를 추출하는 함수

#     Args:
#         url (str): crawling할 웹페이지의 URL

#     Returns:
#         tuple:
#             - str: 추출된 본문 텍스트 (없으면 대체 문자열 반환)
#             - str or None: 대표 이미지 URL (없으면 None)
#     """
#     try:
#         # Request Web page
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
        
#     except requests.RequestException as e:
#         print(f"[Error] Failed to Crawl {url}: {e}")
#         return "Cannot Crawling page", None
    
#     # HTML Parsing
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # 1. 본문 후보 영역 찾기
#     main_candidates = soup.find_all(
#         ['article', 'main', 'section', 'div'],
#         attrs={'id': re.compile(r'(content|main)', re.I),
#                'class': re.compile(r'(content|main|article|post)', re.I)}
#     )
#     if not main_candidates:
#         main_candidates = [soup.body]  # fallback
        
#     # 2. 후보들 중에서 텍스트가 가장 많은 블록을 선택
#     best_block = max(main_candidates, key=lambda tag: len(tag.get_text(strip=True)))

#     # 3. 블록 내부에서 유의미한 텍스트 수집
#     text_elements = best_block.find_all(['p', 'div', 'span'])
    
#     # 4. 전처리: 중복 제거 및 불필요한 내용 필터링
#     seen = []
#     clean_paragraphs = []
#     for el in text_elements:
#         text = el.get_text(separator=" ", strip=True)
#         text = re.sub(r'\s+', ' ', text)

#         if len(text) < 30:
#             continue

#         if re.search(r'(구독|저작권|관련 기사|더 보기|클릭|로그인)', text, re.I):
#             continue

#         # 중복 및 유사도 기반 필터링
#         if any(is_similar(text.lower(), existing.lower()) for existing in seen):
#             continue

#         seen.append(text)
#         clean_paragraphs.append(text)

#     content_text = "\n\n".join(clean_paragraphs) if clean_paragraphs else "No meaningful content found."
    
#     # 5. 대표 이미지 찾기
#     image_url = None
#     og_image = soup.find("meta", property="og:image")
#     if og_image and og_image.get("content"):
#         image_url = og_image["content"]

#     return content_text, image_url

import requests
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from typing import Dict, Tuple, Optional
import json

def is_similar(a: str, b: str, threshold: float = 0.9) -> bool:
    """
    두 문자열의 유사도를 계산하여 threshold 이상이면 True 반환
    
    Args:
        a (str): 비교할 첫 번째 문자열
        b (str): 비교할 두 번째 문자열
        threshold (float): 유사도 임계값 (기본값: 0.9)
        
    Returns:
        bool: 유사도가 threshold 이상이면 True, 아니면 False
    """
    return SequenceMatcher(None, a, b).ratio() > threshold

def extract_metadata(soup: BeautifulSoup) -> Dict[str, str]:
    """
    웹페이지의 메타데이터를 추출하는 함수
    
    Args:
        soup (BeautifulSoup): 파싱된 HTML 객체
        
    Returns:
        Dict[str, str]: 추출된 메타데이터 딕셔너리
    """
    metadata = {}
    
    # 제목 추출
    title = soup.find('title')
    if title:
        metadata['title'] = title.text.strip()
    
    # Open Graph 메타데이터 추출
    og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
    for tag in og_tags:
        key = tag.get('property', '').replace('og:', '')
        value = tag.get('content', '')
        if key and value:
            metadata[key] = value
    
    # 일반 메타데이터 추출
    meta_tags = soup.find_all('meta', attrs={'name': True})
    for tag in meta_tags:
        key = tag.get('name', '')
        value = tag.get('content', '')
        if key and value:
            metadata[key] = value
            
    return metadata

def find_main_content(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """
    웹페이지에서 본문이 있을 것으로 예상되는 영역을 찾는 함수
    
    Args:
        soup (BeautifulSoup): 파싱된 HTML 객체
        
    Returns:
        Optional[BeautifulSoup]: 본문 영역으로 추정되는 BeautifulSoup 객체
    """
    # 본문 후보 영역 찾기
    main_candidates = soup.find_all(
        ['article', 'main', 'section', 'div'],
        attrs={
            'id': re.compile(r'(content|main|article|post|body)', re.I),
            'class': re.compile(r'(content|main|article|post|body)', re.I)
        }
    )
    
    if not main_candidates:
        main_candidates = [soup.body] if soup.body else []
    
    if not main_candidates:
        return None
        
    # 텍스트 길이와 구조적 중요도를 고려하여 최적의 본문 영역 선택
    def score_block(block):
        text_length = len(block.get_text(strip=True))
        # 구조적 중요도 점수 (article > main > section > div)
        structure_score = {
            'article': 4,
            'main': 3,
            'section': 2,
            'div': 1
        }.get(block.name, 0)
        return text_length * (1 + structure_score * 0.1)
    
    return max(main_candidates, key=score_block)

def clean_text(text: str) -> str:
    """
    텍스트를 정제하는 함수
    
    Args:
        text (str): 정제할 텍스트
        
    Returns:
        str: 정제된 텍스트
    """
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    # HTML 엔티티 디코딩
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    return text.strip()

def crawl_url(url: str) -> Tuple[Dict[str, str], str, Optional[str]]:
    """
    주어진 URL을 크롤링하여 메타데이터, 본문 텍스트, 대표 이미지를 추출하는 함수

    Args:
        url (str): 크롤링할 웹페이지의 URL

    Returns:
        Tuple[Dict[str, str], str, Optional[str]]:
            - Dict[str, str]: 추출된 메타데이터
            - str: 추출된 본문 텍스트
            - Optional[str]: 대표 이미지 URL (없으면 None)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
    except requests.RequestException as e:
        print(f"[Error] Failed to Crawl {url}: {e}")
        return {}, "Cannot Crawling page", None
    
    # HTML Parsing
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 메타데이터 추출
    metadata = extract_metadata(soup)
    
    # 본문 영역 찾기
    main_content = find_main_content(soup)
    if not main_content:
        return metadata, "No main content found", None
    
    # 본문 내 텍스트 요소 수집
    text_elements = main_content.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    # 전처리: 중복 제거 및 불필요한 내용 필터링
    seen = []
    clean_paragraphs = []
    
    for el in text_elements:
        text = clean_text(el.get_text(separator=" ", strip=True))
        
        # 너무 짧은 텍스트 제외
        if len(text) < 30:
            continue
            
        # 불필요한 내용 필터링
        if re.search(r'(구독|저작권|관련 기사|더 보기|클릭|로그인|댓글|공유하기)', text, re.I):
            continue
            
        # 중복 및 유사도 기반 필터링
        if any(is_similar(text.lower(), existing.lower()) for existing in seen):
            continue
            
        seen.append(text)
        clean_paragraphs.append(text)
    
    content_text = "\n\n".join(clean_paragraphs) if clean_paragraphs else "No meaningful content found."
    
    # 대표 이미지 찾기
    image_url = None
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image_url = og_image["content"]
    
    return metadata, content_text, image_url

