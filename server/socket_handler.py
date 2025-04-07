import asyncio
import io
from aiohttp import web
import os
from pydub import AudioSegment
from whisper_transcriber import onpenai_speech

async def handle_media_stream(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("✅ WebSocket Client Connected")

    audio_buffer = io.BytesIO()

    async for msg in ws:
        if msg.type == web.WSMsgType.BINARY:
            audio_data = msg.data
            print(f"🎵 Received {len(audio_data)} bytes of audio data")
            audio_buffer.write(audio_data)

    # WebSocket 종료 후 실행되도록 수정
    total_bytes = audio_buffer.getbuffer().nbytes

    if total_bytes > 0:
        audio_buffer.seek(0)
        audio_segment = AudioSegment.from_file(audio_buffer, format="webm")
        audio_segment.export("output.wav", format="wav")
        onpenai_speech("./output.wav")

    print("❌ WebSocket Client Disconnected")
    return ws
