import requests
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a, b).ratio() > threshold

def crawl_url(url):
    """
    주어진 URL을 크롤링하여 본문에 가까운 텍스트와 대표 이미지를 추출하는 함수

    Args:
        url (str): crawling할 웹페이지의 URL

    Returns:
        tuple:
            - str: 추출된 본문 텍스트 (없으면 대체 문자열 반환)
            - str or None: 대표 이미지 URL (없으면 None)
    """
    try:
        # Request Web page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
    except requests.RequestException as e:
        print(f"[Error] Failed to Crawl {url}: {e}")
        return "Cannot Crawling page", None
    
    # HTML Parsing
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. 본문 후보 영역 찾기
    main_candidates = soup.find_all(
        ['article', 'main', 'section', 'div'],
        attrs={'id': re.compile(r'(content|main)', re.I),
               'class': re.compile(r'(content|main|article|post)', re.I)}
    )
    if not main_candidates:
        main_candidates = [soup.body]  # fallback
        
    # 2. 후보들 중에서 텍스트가 가장 많은 블록을 선택
    best_block = max(main_candidates, key=lambda tag: len(tag.get_text(strip=True)))

    # 3. 블록 내부에서 유의미한 텍스트 수집
    text_elements = best_block.find_all(['p', 'div', 'span'])
    
    # 4. 전처리: 중복 제거 및 불필요한 내용 필터링
    seen = []
    clean_paragraphs = []
    for el in text_elements:
        text = el.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text)

        if len(text) < 30:
            continue

        if re.search(r'(구독|저작권|관련 기사|더 보기|클릭|로그인)', text, re.I):
            continue

        # 중복 및 유사도 기반 필터링
        if any(is_similar(text.lower(), existing.lower()) for existing in seen):
            continue

        seen.append(text)
        clean_paragraphs.append(text)

    content_text = "\n\n".join(clean_paragraphs) if clean_paragraphs else "No meaningful content found."
    
    # 5. 대표 이미지 찾기
    image_url = None
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image_url = og_image["content"]

    return content_text, image_url
