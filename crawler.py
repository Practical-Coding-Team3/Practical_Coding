import requests
from bs4 import BeautifulSoup

def crawl_url(url):
    """
    주어진 URL에서 웹페이지의 본문 텍스트(기사 내용 등)을 추출하는 함수

    Args:
        url (str): crawling할 웹페이지의 URL

    Returns:
        str: 추출된 본문 텍스트 (없을 경우 대체 문자열 반환)
    """
    try:
        # 웹페이지 요청
        response = requests.get(url, timeout=10)
        response.raise_for_status() # 응답 에러 시 예외 발생
        
        # HTML parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 본문 텍스트 찾기
        # test용 -> p tag 기준으로 crawling
        # 이후 알고리즘적으로 crawling 구현하기
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        if not text.strip():
            return "No contents in this page"
        
        return text
    
    except Exception as e:
        print(f"[Error] Failed to crawl {url}: {e}")
        return "No contents in tihs page"