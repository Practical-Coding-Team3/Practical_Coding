from fastapi import FastAPI
from routers import text_api
from routers import Summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP Method 허용
    allow_headers=["*"],  # 모든 HTTP Header 허용
)


app.include_router(text_api.router)
app.include_router(Summary.router)
