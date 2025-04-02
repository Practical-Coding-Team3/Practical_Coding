import api, text_correction

textT = "음...내가 오늘 우산을 챙길지 고민이야. 비가 오는 지 확인해줘" # 음성을 가져왔다고 가정

query = text_correction.text_correction(text)
api.api_request(query)