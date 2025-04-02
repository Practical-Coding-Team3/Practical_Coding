from konlpy.tag import Okt

RAW_TEXT_1 = "음...오늘 날씨 날씨가 궁금해 어디 날씨냐면 춘천 날씨 오늘 춘천 날씨가 궁금해"
RAW_TEXT_2 = "음...내가 오늘 우산을 챙길지 고민이야. 춘천에 비가 오는 지 확인해줘"
RAW_TEXT_3 = "음...오늘 날씨가 궁금해. 어...춘천에 미세먼지가 많은지 확인해줘"
RAW_TEXT_4 = "어...내가 갑자기 궁금한게 생겼는데 사과에 대해서 검색해줘"


def text_correction(text):
    # 불필요한 문자 필터
    stopwords = [
        "음", "어", "것", "거", "수", "좀", "같은", "정도", "요청", "내용",
        "어디", "누구", "디", "면", "게", "냐", "가", "이", "그", "저"
    ]

    keyword_priority = {
        "장소": ["춘천", "서울", "부산", "제주", "대구"],  # 확장 가능
        "주제": ["미세먼지", "날씨", "기온", "강수", "비", "눈", "풍속"],
        "행동": ["확인하다", "찾다", "알다", "검색하다", "궁금하다"]
    }

    okt = Okt()
    pos = okt.pos(text)

    print(pos)
    # 명사, 동사, 형용사
    allow_pos = ['Noun', 'Verb', 'Adjective']

    # 중복 및 불필요한 문자 제거
    filtered = [
        word for word, tag in pos
        if tag in allow_pos and word not in stopwords and len(word) > 1     # 명사, 동사, 형용사만 남김, stopwords 및 1글자 삭제
    ]
    filtered = list(dict.fromkeys(filtered)) # 중복 제거

    priority_words = []
    for cat in ["장소", "주제", "행동"]:
        for kw in keyword_priority[cat]:
            if kw in filtered:
                priority_words.append(kw)

    print("전체 단어: ", filtered)
    length_hint = int(len(filtered))

    core_word = " ".join(filtered[:length_hint])
    print("핵심 단어:", core_word)
    return core_word

if __name__ == "__main__":
    text = text_correction(RAW_TEXT_2)

