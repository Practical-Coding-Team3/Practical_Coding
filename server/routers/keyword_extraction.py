from konlpy.tag import Hannanum
from server.routers.api import add_category
import json

"""
text에서 core_words 찾기
core_words: text의 명사들
"""

RAW_TEXT = "비가 오는지 확인해봐"  # 테스트용 문자열 1
JSON_PATH = "./server/routers/category_map.json"
#JSON_PATH = "category_map.json"  # JSON 파일 경
def filter_pos(pos, allow_pos):
    # 품사 필터링
    return [word for word, tag in pos if tag in allow_pos]

def remove_stopwords(words):
    # 불용어 제거
    stopwords = [ # 불필요한 문자 필터
        "음", "어", "것", "거", "수", "좀", "같은", "정도", "요청", "내용",
        "어디", "누구", "디", "면", "게", "냐", "가", "이", "그", "저"
    ]
    return [word for word in words if word not in stopwords]

def find_category(core_words, json_path=JSON_PATH):
    with open(json_path, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    index = category_dict.get("index", {})
    for word in core_words:
        if word in index:
            return index[word]
    return "Failed"

def get_related_info(category, ):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    category_info = category_dict.get("category_info", {})
    return category_info.get(category, {}).get("related", [])


def get_category_and_related_info(filtered, json_path=JSON_PATH):
    """
    filtered에서 한 단어씩 카테고리 찾기
    :param filtered: N인 단어들
    :param json_path: JSON 파일 경로
    :return: category, related_info
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        category_dict = json.load(f)

    index = category_dict.get("index", {})
    category_info = category_dict.get("category_info", {})

    for word in filtered:
        if word in index:
            category = index[word]
            related_info = category_info.get(category, {}).get("related", [])
            return category, related_info
    return "기타", []

def extract_with_konlpy(text):
    hananum = Hannanum()
    pos = hananum.pos(text)

    # allow_pos = ['N', 'P', 'A']  # Hannanum 품사 태그
    allow_pos = 'N'
    core_words = filter_pos(pos, allow_pos)
    core_words = remove_stopwords(core_words)
    core_words = list(dict.fromkeys(core_words))

    category = get_category_and_related_info(core_words)
    print(core_words, category)
    if category == "Failed":
        print(add_category(core_words))

    return core_words

def extract_with_bm25(text):
    return 0

def keyword_extraction(text):
    if len(text) < 100:  # 길이 기준 (문자 수)
        return extract_with_konlpy(text)
    else:
        return extract_with_bm25(text)


if __name__ == "__main__":
    text = keyword_extraction(RAW_TEXT)

    print(text)

