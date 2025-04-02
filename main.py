import api, text_correction

FILE = "./whisper_text"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.readline()

core_word = text_correction.text_correction(text) # 핵심 단어 뽑아내기
print("\n\n")
api.api_request(core_word) # 뽑아낸 핵심 단어 LLM에 입력