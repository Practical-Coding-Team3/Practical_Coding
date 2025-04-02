from konlpy.tag import Okt

raw_text_1 = "음...오늘 날씨 날씨가 궁금해 어디 날씨냐면 춘천 날씨 오늘 춘천 날씨가 궁금해"
raw_text_2 = "음...내가 오늘 우산을 챙길지 고민이야. 비가 오는 지 확인해줘"

def text_correction(text):
    # 불필요한 문자
    stopwords = ["음", "것", "거", "수", "좀", "같은", "정도", "정보", "요청", "내용", "어디", "누구"]

    okt = Okt()
    nouns = okt.nouns(text)

    # 중복 및 불필요한 문자 제거
    filtered = [
        noun for noun in nouns
        if noun not in stopwords and len(noun) > 1
    ]
    filtered = list(dict.fromkeys(filtered))  # 순서 유지한 중복 제거

    # 검색 쿼리 생성 (길이 제한 가능)
    query = " ".join(filtered[:3])  # 상위 3개만 조합
    print("생성된 검색 쿼리:", query)
    return query

if __name__ == "__main__":
    text = text_correction(raw_text_2)

