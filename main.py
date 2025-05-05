from crawler import crawl_url
from summarizer import summarize_text_first, summarize_text_remain
import json
from typing import List, Dict, Optional


def load_urls(file_path: str) -> List[str]:
    """
    텍스트 파일에서 URL 목록을 읽어 리스트로 반환한다.

    Args:
        file_path (str): URL이 저장된 text 파일 경로

    Returns:
        list[str]: 줄바꿈을 제거한 URL 문자열 리스트
    """
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def process_url(url: str, is_first: bool = False) -> Dict[str, str]:
    """
    URL을 크롤링하고 요약하는 함수

    Args:
        url (str): 처리할 URL
        is_first (bool): 첫 번째 URL인지 여부 (자세한 요약 사용)

    Returns:
        Dict[str, str]: 처리 결과를 담은 딕셔너리
    """
    print(f"\n🔗 Processing URL: {url}")
    
    # Crawling
    metadata, body_text, image_url = crawl_url(url)
    
    # Summary
    if is_first:
        summary = summarize_text_first(body_text, metadata)
    else:
        summary = summarize_text_remain(body_text)
    
    return {
        'url': url,
        'metadata': metadata,
        'summary': summary,
        'image_url': image_url
    }
    
def save_results(results: List[Dict[str, str]], output_file: str = 'results.json'):
    """
    처리 결과를 JSON 파일로 저장하는 함수

    Args:
        results (List[Dict[str, str]]): 저장할 결과 리스트트
        output_file (str, optional): 저장할 파일 경로
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent = 2)

def main():
    """
    메인 함수 : URL 목록을 읽어 크롤링하고 요약한 후 결과를 저장
    """
    # URL load
    file_path = 'url.txt'
    urls = load_urls(file_path)
    print("✅ Loaded URLs:")
    for url in urls:
        print(f" - {url}")
        
    # 각 URL 처리
    results = []
    for i, url in enumerate(urls):
        result = process_url(url, is_first = (i == 0))
        results.append(result)
        
        # 결과 출력
        print("\n📝 Summary:")
        print(result['summary'])
        if result['image_url']:
            print(f"\n🖼️  Image URL: {result['image_url']}")
        print("\n" + "="*100)
        
    # 결과 저장
    save_results(results)
    print("\n✅ Results saved to results.json")
    
               
if __name__ == "__main__":
    main()