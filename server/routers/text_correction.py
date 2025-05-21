from konlpy.tag import Hannanum
import json

RAW_TEXT = "오늘 춘천 날씨에 대해서 알려줘"  # 테스트용 문자열 1
JSON_PATH = "./server/routers/category_map.json"

def filter_pos(pos, allow_pos):
    # 품사 필터링
    return [word for word, tag in pos if tag in allow_pos]

def remove_stopwords(words):
    # 불용어 제거
    stopwords = [ # 불필요한 문자 필터
        "음", "어", "것", "거", "수", "좀", "같은", "정도", "요청", "내용",
        "어디", "누구", "디", "면", "게", "냐", "가", "이", "그", "저"
    ]
    return [word for word in words if word not in stopwords and len(word) > 1]

def find_category(core_words):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    index = category_dict.get("index", {})
    for word in core_words:
        if word in index:
            return index[word]
    return "Failed"

def get_category_and_related_info(core_words, json_path=JSON_PATH):
    with open(json_path, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    for category, content in category_dict.items():
        keywords = content.get("keywords", [])
        if any(word in keywords for word in core_words):
            related_info = content.get("related", [])
            return category, related_info

    return "기타", []

def get_related_info(category, ):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    category_info = category_dict.get("category_info", {})
    return category_info.get(category, {}).get("related", [])

def text_correction(text):
    hananum = Hannanum()
    pos = hananum.pos(text)

    #allow_pos = ['N', 'P', 'A']  # Hannanum 품사 태그
    allow_pos = 'N'
    filtered = filter_pos(pos, allow_pos)
    filtered = remove_stopwords(filtered)
    filtered = list(dict.fromkeys(filtered))

    category = find_category(filtered)
    if category == "Failed":
        print("카테고리 찾기 실패")
        return "Failed"

    core_word = " ".join(filtered)
    return core_word


if __name__ == "__main__":
    text = text_correction(RAW_TEXT)
    print(text)

