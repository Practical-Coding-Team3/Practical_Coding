import requests

url = "http://127.0.0.1:8000/text/"
data = {"text": "내일 춘천 날씨에 대해 알려줘"}

response = requests.post(url, json=data)

# 응답 확인
if response.status_code == 200:
    print("JSON 응답:", response.json())
else:
    print("서버 응답 오류")