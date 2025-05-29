from konlpy.tag import Hannanum
from server.routers.api import add_category, add_related_word
import json
"""
text에서 core_words 찾기
core_words: text의 명사들
"""

JSON_PATH = "./server/utils/category_map.json"
#JSON_PATH = "category_map.json"  # JSON 파일 경
def filter_pos(pos, allow_pos):
    # 품사 필터링
    return [word for word, tag in pos if tag in allow_pos]

def remove_action_nouns(words):
    action_word = ""
    action_nouns = ["검색", "조회", "확인", "설명", "추천", "정보", "알림", "질문", "내용"]

    for word in words:  # 행위 단어 추출
        if word in action_nouns:
            action_word = word + " "
            words.remove(word)

    return words, action_word

def remove_stopwords(words):
    # 불용어 제거
    stopwords = [ # 불필요한 문자 필터
        "내", "음", "어", "것", "거", "수", "좀", "같은", "정도", "요청", "내용",
        "어디", "누구", "디", "면", "게", "냐", "가", "이", "그", "저", "뭐", "뭔지"
    ]
    return [word for word in words if word not in stopwords]

def get_related_info(category, json_path=JSON_PATH):
    """
    카테고리 추가 -> 관련 단어 찾기
    """
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
    return "해당 없음", []

def not_found_category(core_word, json_path=JSON_PATH):
    category = add_category(core_word)
    #category = new_category.split(":")[1].strip()

    with open(JSON_PATH, 'r+', encoding='utf-8') as f:
        category_dict = json.load(f)
        if "index" not in category_dict:
            category_dict["index"] = {}
        if isinstance(core_word, list):
            for word in core_word:
                category_dict["index"][word] = category
        else:
            category_dict["index"][core_word] = category
        f.seek(0)
        json.dump(category_dict, f, ensure_ascii=False, indent=4)
        f.truncate()

    return category

def not_found_related_word(category, json_path=JSON_PATH):
    new_related_word = add_related_word(category)
    new_related_word_list = [word.strip() for word in new_related_word.split(',')]

    with open(json_path, 'r+', encoding='utf-8') as f:
        category_dict = json.load(f)
        if category not in category_dict["category_info"]:
            category_dict["category_info"][category] = {"related": []}

        category_dict["category_info"][category]["related"] = new_related_word_list
        f.seek(0)
        json.dump(category_dict, f, ensure_ascii=False, indent=4)
        f.truncate()

    return new_related_word_list

def keyword_extraction(text):
    hananum = Hannanum()
    pos = hananum.pos(text)

    action_word = "" # 행위 단어
    # allow_pos = ['N', 'P', 'A']  # Hannanum 품사 태그
    allow_pos = 'N'
    core_words = filter_pos(pos, allow_pos)
    core_words = remove_stopwords(core_words)
    core_words = list(dict.fromkeys(core_words))

    core_words, action_word = remove_action_nouns(core_words)  # 행위 단어 제거
    category = get_category_and_related_info(core_words)

    if category == "Failed":
        add_category(core_words)

    return core_words, action_word
