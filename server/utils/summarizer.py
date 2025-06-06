from typing import List
from dotenv import load_dotenv

import os
import google.generativeai as genai

# .env 파일에서 API key 받아오기
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")

# Gemini API 초기화
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def split_text(text: str, max_length: int = 30000) -> List[str]:
    """
    프롬프트로 하기에는 너무 긴 텍스트를 최대 길이에 맞춰 여러 개의 청크로 나누는 함수

    Args:
        text (str): 나눌 텍스트
        max_length (int): 각 청크의 최대 길이

    Returns:
        List[str]: 나눠진 텍스트 청크 리스트
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    paragraphs = text.split('\n\n')
    current_chunk = []
    current_length = 0
    
    for paragraph in paragraphs:
        if current_length + len(paragraph) > max_length:
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
            current_chunk = [paragraph]
            current_length = len(paragraph)
        else:
            current_chunk.append(paragraph)
            current_length += len(paragraph)
            
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
        
    return chunks


def summarize_text_first(text: str) -> str :
    """
    주어진 본문을 Gemini API를 통해 자세히 요약하는 함수
    (뉴스, 공지, 블로그 등 모든 종류의 본문에 대해 동작)

    Args:
        text (str): 요약하고자 하는 원문 텍스트

    Returns:
        str: Gemini가 생성한 요약 결과
    """
    try:
        # 텍스트가 너무 길 경우 나누어서 처리
        chunks = split_text(text)
        summaries = []
        
        for i, chunk in enumerate(chunks):
            # 첫 번째 청크에 대한 프롬프트
            if i == 0:
                prompt = f"""
                아래 본문을 요약해주세요. 요약시 다음과 같은 형식으로 해주세요
                가장 핵심적인 한 줄 요약(굵게)
                핵심 내용을 2~4문단으로 요약 (본문 요약)   
                ---
                
                {chunk}
                """
            else:
                prompt = f"""
                다음은 이전 요약에 이어지는 나머지 부분입니다.
                이전 요약과 연결하여 전체 내용을 보완해주세요:
                
                {chunk}
                """
        
            response = model.generate_content(prompt)
            summaries.append(response.text.strip())
            
        return "\n\n".join(summaries)

    except Exception as e:
        print(f"[Error] Failed to summarize: {e}")
        return "Failed to summarize"
    
    
def summarize_text_remain(text: str) -> str:
    """
    주어진 본문을 요약하여 3줄의 핵심 헤드라인 형태로 요약하는 함수

    이 함수는 다음과 같은 포맷으로 결과를 반환한다:
    1. "첫 번째 핵심 요약"
    2. "두 번째 핵심 요약"
    3. "세 번째 핵심 요약"

    Args:
        text (str): 요약하고자 하는 원본 텍스트. (뉴스, 기사, 보고서 등)

    Returns:
        str: Gemini 모델이 생성한 3줄 요약 결과 (문장 번호 포함).
             에러가 발생할 경우 "Failed to summarize"를 반환.
    """
    try:
        # 텍스트가 너무 길 경우 나누어서 처리
        chunks = split_text(text)

        # 나뉜 청크들을 다시 하나의 문자열로 합쳐서 전체 내용을 전달
        combined_text = "\n\n".join(chunks)

        # Gemini 모델에 전달할 프롬프트 구성
        prompt = f"""
        다음 기사를 3줄의 헤드라인으로 요약해주세요.
        각 문장은 번호와 큰따옴표로 구분해서 출력해 주세요. (예: 1. "내용" 2. "내용" ...)

        {combined_text}
        """

        # Gemini 모델에 요약 요청
        response = model.generate_content(prompt)

        # 결과 텍스트 정리 후 반환
        return response.text.strip()

    except Exception as e:
        # 에러 발생 시 콘솔 출력 후 예외 메시지 반환
        print(f"[Error] Failed to summarize: {e}")
        return "Failed to summarize"