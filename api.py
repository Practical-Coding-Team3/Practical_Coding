from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_ID = "gemini-2.0-flash"

TEST_TEXT_1 = "오늘 춘천시 날씨는 어때?" # 테스트용 문자열 1
TEST_TEXT_2 = "강원대 주변 음식점 찾아줘" # 테스트용 문자열 2


def api_request(text):
    client = genai.Client(api_key=API_KEY)

    google_search_tool = Tool(
        google_search=GoogleSearch()
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=text + ", 이모지 제거, markdown을 이용한 글 강조 제거, 제일 상단 키워드 출력",
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )

if __name__ == "__main__":
    api_request(TEST_TEXT_1)