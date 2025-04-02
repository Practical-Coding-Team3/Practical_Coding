from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

API_KEY: str = "AIzaSyBg2BUbeNqBn92jqy7Cp34Q5LrbSWMAT8E"
MODEL_ID = "gemini-2.0-flash"

test_text = "오늘 춘천시 날씨는 어때?"

def api_request(text):
    client = genai.Client(api_key=API_KEY)

    google_search_tool = Tool(
        google_search=GoogleSearch()
    )
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=text,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )

    print(response.text)
    # for each in response.candidates[0].content.parts:
    #     print(each.text)
    # print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)

if __name__ == "__main__":
    api_request(test_text)