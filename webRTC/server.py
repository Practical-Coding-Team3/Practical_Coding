import asyncio 
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiohttp import web
import json

# webRTC server 정의
class WebRTCServer:
    def __init__(self):
        # RTC 연결 객체를 저장할 변수
        self.pc = None
    
    # client에서 offer를 받는 POST method
    async def offer(self, request):
        # client로부터 받은 JSON 형식의 offer 정보 parsing
        params = await request.json()
        offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])
        
        # RTC 연결을 위한 객체 생성
        pc = RTCPeerConnection()
        pc_id = "PeerConnection"
        self.pc = pc
        
        # ICE connection state가 변경될 때마다 상태를 출력하는 콜백 함수 설정
        @pc.on("iceconnectionstatechange")
        def on_iceconnectionstatechange():
            print(f"ICE connection state: {pc.iceConnectionState}")
        
        # track(voice or video track)을 수신했을 때 호출되는 콜백 함수 설정
        @pc.on("track")
        def on_track(track):
            if track.kind == "audio":
                print("Audio track received!")
        
        # client에서 제공한 offer를 받아 RTC 연결을 설정
        await pc.setLocalDescription(offer)
        
        # answer를 생성하고 local에서 사용할 answer를 설정
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        
        # 생성된 answer를 client에 json 형태로 응답
        return web.Response(
            content_type = "application/json",
            text = json.dumps({
                "sdp": pc.localDescription.sdp,
                "type": pc.localDescription.type
            })
        )
        
      
# web server 설정정 
app = web.Application()

# webRTC server instance를 생성하고 '/offer'경로에 대한 요청을 처리하는 router를 추가
webrtc_server = WebRTCServer()
app.router.add_post("/offer", webrtc_server.offer)

# server execution (8080 port)
if __name__ == "__main__" :
    web.run_app(app, port=8080)

