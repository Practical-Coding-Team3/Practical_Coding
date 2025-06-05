import os
from fastapi import APIRouter, Request, HTTPException
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # OPENAI_API_KEY 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/keyword", tags=["keyword"])

@router.post("/explain")
async def explain_word(request: Request):
    """
    단어 하나를 받아서 GPT 모델을 통해 쉬운 설명을 생성
    요청 형식: { "word": "양자역학" }
    응답 형식: { "summary": "양자역학은..." }
    """
    try:
        # 요청 JSON에서 word 추출
        data = await request.json()
        word = data.get("word", "").strip()

        if not word:
            raise HTTPException(status_code=400, detail="word 필드가 비어 있음")

        # 프롬프트 작성
        prompt = f"""
            "{word}"의 개념을 인터넷 조사 결과를 근거로 일반인이 이해할 수 있도록 간결하고 명확하게 설명해줘.
            절대로 "다음은 ..." 같은 안내 문구나 형식적인 말은 포함하지 말고,
            설명만 자연스럽게 문장으로 알려줘.
            """

        # GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )

        result = response.choices[0].message.content.strip()
        return {"summary": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류 발생: {str(e)}")