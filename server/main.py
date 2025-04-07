import asyncio
import os
from aiohttp import web
import io
import wave
from pydub import AudioSegment
import time
import torch
import whisper
from socket_handler import handle_media_stream


app = web.Application()
app.add_routes([web.get("/media-stream", handle_media_stream)])

if __name__ == "__main__":
    web.run_app(app, port=8000) 