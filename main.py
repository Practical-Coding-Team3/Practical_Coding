from crawler import crawl_url
from summarizer import summarize_text

# 수집된 URL들을 불러오는 함수
def load_urls(file_path):
    """
    텍스트 파일에서 URL 목록을 읽어 리스트로 반환한다.

    Args:
        file_path (str): URL이 저장된 text 파일 경로

    Returns:
        list: 줄바꿈을 제거한 URL 문자열 리스트
    """
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls


def main():
    file_path = 'url.txt'
    urls = load_urls(file_path)
    print("URL list : ", urls)
    
    
    for url in urls:
        print(f"\n🔗 Crawling: {url}")
        text = crawl_url(url)
        
        # crawling test -> 일단 크롤링한 데이터 중 앞의 300 단어만
        print(f"📄 Extracted text (first 300 chars):\n{text[300:]}\n")
    
        # summarize test
        summary = summarize_text(text)
        print(f"🧠 Summary:\n{summary}")
        print("-" * 60)
        
        
        
if __name__ == "__main__":
    main()