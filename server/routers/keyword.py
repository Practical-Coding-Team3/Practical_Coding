import json
import re
from fastapi import APIRouter, Request, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/keyword", tags=["keyword"])


@router.post("/")
async def receive_text(request: Request):
    try:
        # raw body를 먼저 가져와서 수동으로 처리
        raw_body = await request.body()
        body_str = raw_body.decode('utf-8')
        
        # JSON 형태인지 확인
        if body_str.strip().startswith('{') and body_str.strip().endswith('}'):
            # "text":"..." 패턴을 찾아서 텍스트 추출
            match = re.search(r'"text"\s*:\s*"(.+)"', body_str, re.DOTALL)
            if match:
                text = match.group(1)
                # 이스케이프된 따옴표는 복원
                text = text.replace('\\"', '"')
                text = text.strip()
                
                print(f"Received text: {text}")
                prompt = f"""
                    다음 텍스트에서 사람들이 잘 모를 법한 어려운 단어 또는 전문용어만 JSON 배열 형식으로 뽑아줘:
                    {text}
                    """
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=300,
                )
                result = response.choices[0].message.content
                return {"received_text": result}
            
            else:
                return {"error": "text field not found in JSON"}
        else:
            # JSON이 아닌 경우 그대로 텍스트로 처리
            text = body_str.strip()
            prompt = f"""
                    다음 텍스트에서 사람들이 잘 모를 법한 어려운 단어 또는 전문용어만 JSON 배열 형식으로 뽑아줘:
                    {text}
                    """
            response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=300,
            )
            result = response.choices[0].message.content
            return {"received_text": result}    
    except Exception as e:
        # 기존 방식도 시도해보기
        try:
            data = await request.json()
            text = data.get("text", "")
            if not isinstance(text, str):
                return {"error": "text must be a string"}
            
            processed_text = text.strip()
            prompt = f"""
                    다음 텍스트에서 사람들이 잘 모를 법한 어려운 단어 또는 전문용어만 JSON 배열 형식으로 뽑아줘:
                    {processed_text}
                    """
            response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=300,
            )
            result = response.choices[0].message.content
            return {"received_text": result}
        except:
            return {"error": f"Failed to process request: {str(e)}"}







