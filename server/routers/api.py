from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_ID = "gemini-2.0-flash"

def add_category(keyword):
    client = genai.Client(api_key=API_KEY)
    print(keyword)
    prompt = (
        f'"{keyword}"가 어떤 카테고리에 속하는지 명사로 딱 하나 말해'
        '그리고 그에 맞는 연관 단어들을 3개씩 알려줘.'
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=GenerateContentConfig(
            response_modalities=["TEXT"],
        )
    )

    return response.text.strip()

def related_url(keyword, related_word):
    client = genai.Client(api_key=API_KEY)
    google_search_tool = Tool(
        google_search=GoogleSearch()
    )

    prompt = (
        f'"{keyword}"에 관한 정보와 {keyword}와 관련된 키워드 {related_word} 각각에 대해 '
        '실제 한국어 웹사이트 URL을 알려줘. 형식은 다음처럼 정리해줘:'
        'Main: URL - sub1: URL - sub2: URL - sub3 : URL'
        '다른 말은 하지말고 오직 URL만 알려줘.'
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents= prompt,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )
    return response.text.strip()


if __name__ == "__main__":
    text = "오늘 춘천 날씨에 대해서 알려줘"
    response = related_url("사과", ["함유량", "요리", "네이버 쇼핑"])
    print(response)
    # related_word = "춘천 날씨"
    # url = related_url(related_word)
    # print(url)
