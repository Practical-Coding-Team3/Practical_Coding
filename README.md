# Practical_Coding
URL 획득 -> Crawling -> 요약 및 본문 내용 추출

# main.py
load_urls : url.txt에서 url을 읽어오는 함수

process_url : crawler.py와 summarizer.py를 이용하여 url을 크롤링하고 요약하는 함수

save_results : 처리 결과를 JSON 파일로 저장하는 함수

# url.txt
크롤링할 url : 현재는 임의로 txt 파일을 설정 추후 단어 추출을 바탕으로 url 획득할 예정

# crawler.py
crawl_url : URL을 인자로 받아 메타데이터, 본문 텍스트, 대표 이미지를 추출하는 함수

extract_metadata : 웹페이지 내의 메타데이터들을 추출하는 함수

find_main_content : 웹페이지 내에서 본문으로 예상되는 영역을 찾는 함수

clean_text : 추출한 텍스트를 전처리하는 함수

is_similar : 비슷한 문자열이 있으면 하나만 추출하도록 하는 함수

# summarizer.py
split_text : 프롬프트로 하기에는 너무 긴 텍스트를 최대 길이에 맞춰 여러 개의 청크로 나누는 함수

summarize_text_first : 메인 url에 대해 자세하게 요약해주는 함수

summarize_text_remian : 보조 url에 대해 3줄 요약해주는 함수

# requirements.txt
위의 함수들을 이용할때 설치해야하는 것들
