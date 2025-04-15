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
    print("✅ Loaded URLs:")
    for url in urls:
        print(f" - {url}")
        
    print("\n🚀 크롤링 전체 본문 확인:")
    
    for url in urls:
        print(f"\n🔗 Crawling: {url}")
        body_text, image_url = crawl_url(url)
        
        # 대표 이미지가 있는 경우 출력
        print(f"🖼️  Image: {image_url if image_url else '(없음)'}")

        # 🔽 전체 본문 출력
        print("📄 Extracted Full Text:\n")
        print(body_text)
        print("\n" + "="*100 + "\n")
               
if __name__ == "__main__":
    main()