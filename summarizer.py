import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 API key 받아오기
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API 초기화화
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_text(text):
    """
    주어진 텍스트를 Gemini API를 통해 요약

    Args:
        text (str): 요약하고자 하는 원문 텍스트
        
    Returns:
        str: Gemini가 생성한 요약 결과.
             오류 발생 시 기본 에러 메시지를 반환환
    """
    
    try:
        # 요약 prompt 구성: 지시어 + 본문
        prompt = f"""
        다음 글을 핵심만 간결하게 요약해 주세요: 
        
        {text}
        
        요약: 
        """
        
        # Gemini API에 prompt를 전달하여 응답 받기
        response = model.generate_content(prompt)
        
        # 응답에서 텍스트만 추출해 반환
        return response.text.strip()
    
    except Exception as e:
        print(f"[Error] Failed Summarize: {e}")
        return "Failed Summarize"