# import torch
# import whisper
# import os

# openai_text = ""

# model = whisper.load_model("turbo", device="cuda" if torch.cuda.is_available() else "cpu")

# def onpenai_speech(audio_file_name, model_name="turbo"):
#     global openai_text
#     try:
#         result = model.transcribe(audio_file_name, language="ko")
#         openai_text = result['text']
#     except FileNotFoundError as e:
#         print(f"파일 오류: {e}")
#     except Exception as e:
#         print(f"오류 발생: {e}")
#     finally:
#         if os.path.exists(audio_file_name):
#             os.remove(audio_file_name)
