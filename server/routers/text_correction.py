from konlpy.tag import Hannanum

RAW_TEXT = "오늘 춘천시 날씨는 어때?"  # 테스트용 문자열 1
def filter_pos(pos, allow_pos):
    return [word for word, tag in pos if tag in allow_pos]

def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords and len(word) > 1]

def extract_priority_keywords(words, keyword_priority):
    priority_words = []
    for cat in keyword_priority:
        for kw in keyword_priority[cat]:
            if kw in words:
                priority_words.append(kw)
    return priority_words

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

    hananum = Hannanum()
    pos = hananum.pos(text)
    allow_pos = ['N', 'P', 'A']  # Hannanum 품사 태그
    filtered = filter_pos(pos, allow_pos)
    filtered = remove_stopwords(filtered, stopwords)
    filtered = list(dict.fromkeys(filtered))
    priority_words = extract_priority_keywords(filtered, keyword_priority)
    core_word = " ".join(filtered)
    return core_word


if __name__ == "__main__":
    text = text_correction(RAW_TEXT)

