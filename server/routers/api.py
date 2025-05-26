from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_ID = "gemini-2.0-flash"

def add_related_word(category):
    """
    카테고리를 받아오면 연관 단어 3개를 찾기
    """
    client = genai.Client(api_key=API_KEY)
    google_search_tool = Tool(
        google_search=GoogleSearch()
    )
    prompt = (
        f'"{category}"에 적합한 관련 단어 3개만 쉼표 없이 한 줄로, 따옴표 없이, 다른 말 없이 출력해줘.\n'
        '예: 동물 → 서식지, 종, 특징'
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )
    return response.text.strip()

def add_category(keyword):
    client = genai.Client(api_key=API_KEY)

    prompt = (
        f'"{keyword}"는 어떤 상위 개념의 카테고리에 속하나요? '
        '예를 들어 "사과"는 "과일", "이더리움"은 "블록체인", "기린"은 "동물"처럼요.'
        f'다른 말은 하지 말고 명사인 단어 하나만 말해'
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=GenerateContentConfig(
            response_modalities=["TEXT"],
        )
    )
    return response.text.strip()

def related_url(keyword, related_words):
    """
    related_word: 관련 단어 리스트
    각 관련 단어 마다 반복분 돌려서 keyword + related_word1, 2, 3로 검색
    """
    search_word_1 = keyword + " " + related_words[0]
    search_word_2 = keyword + " " + related_words[1]
    search_word_3 = keyword + " " + related_words[2]

    print(search_word_1, search_word_2, search_word_3)

    client = genai.Client(api_key=API_KEY)
    google_search_tool = Tool(
        google_search=GoogleSearch()
    )
    prompt = (
        f'"{keyword}"에 관한 정보와 {keyword}와 관련된 키워드에 대해'
        '실제 한국어 웹사이트 URL을 알려줘. 형식은 다음처럼 정리해줘:'
        f'Main: {keyword}에 대한 URL - sub1: {search_word_1}에 대한 URL - sub2: {search_word_2}에 대한 URL - sub3 : {search_word_3}에 대한 URL'
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
