# Practical_Coding
URL 획득 -> Crawling -> 요약 및 본문 내용 추출

## 폴더 구조

PRACTICAL_CODING/
├── .env # 환경변수 (GEMINI_API_KEY)
├── .gitignore
├── api.py # FastAPI 서버 (엔드포인트 정의0
├── crawler.py # 웹 크롤링 로직
├── main.py # CLI용 실행 파일 (함수 기반 처리)
├── README.md
├── requirements.txt # 설치 패키지 목록
├── results.json # 처리 결과 저장 파일
├── summarizer.py # Gemini 요약 로직
├── url.txt # 처리할 URL 리스트

### api.py
POST /crawl
- 설명: URL에서 본문 + 메타데이터 + 이미지 추출
- 요청:

```json
{
  "url": "https://example.com/article"
}
```

- 응답:

```json
{
  "metadata": {...},
  "content": "...",
  "image_url": "https://..."
}
```

POST /summarize
- 설명: 텍스트를 요약 (상세 or 3줄 헤드라인)
- 요청:

```json
{
  "text": "여기에 본문 텍스트",
  "detail": true
}
```

- 응답:

```json
{
  "summary": "..."
}
```

POST /process_url
- 설명: URL 하나를 크롤링하고 요약까지 한 번에 처리
- 요청:

```json
{
  "url": "https://example.com/article",
  "is_first": true
}
```

- 응답:

```json
{
  "url": "...",
  "metadata": {...},
  "summary": "...",
  "image_url": "..."
}
```

### main.py
load_urls : url.txt에서 url을 읽어오는 함수

process_url : crawler.py와 summarizer.py를 이용하여 url을 크롤링하고 요약하는 함수

save_results : 처리 결과를 JSON 파일로 저장하는 함수

### url.txt
크롤링할 url : 현재는 임의로 txt 파일을 설정 추후 단어 추출을 바탕으로 url 획득할 예정

### crawler.py
crawl_url : URL을 인자로 받아 메타데이터, 본문 텍스트, 대표 이미지를 추출하는 함수

extract_metadata : 웹페이지 내의 메타데이터들을 추출하는 함수

find_main_content : 웹페이지 내에서 본문으로 예상되는 영역을 찾는 함수

clean_text : 추출한 텍스트를 전처리하는 함수

is_similar : 비슷한 문자열이 있으면 하나만 추출하도록 하는 함수

### summarizer.py
split_text : 프롬프트로 하기에는 너무 긴 텍스트를 최대 길이에 맞춰 여러 개의 청크로 나누는 함수

summarize_text_first : 메인 url에 대해 자세하게 요약해주는 함수

summarize_text_remian : 보조 url에 대해 3줄 요약해주는 함수

### requirements.txt
위의 함수들을 이용할때 설치해야하는 것들


## 실행 방법

### 1. 환경 설정
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. FastAPI 서버 실행
```bash
uvicorn api:app --reload
```
브라우저에서 확인: http://localhost:8000/docs

### 4. CLI 실행 (테스트용)

```bash
python main.py
```