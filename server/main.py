from fastapi import FastAPI
from server.routers import text_api
from server.routers import crawler, summarizer, process_url
from server.routers import Summary
from server.routers import keyword
from server.routers import explain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP Method 허용
    allow_headers=["*"],  # 모든 HTTP Header 허용
)

app.include_router(keyword.router)
app.include_router(text_api.router)
app.include_router(Summary.router)
app.include_router(explain.router)

app.include_router(crawler.router, prefix="/crawl")
app.include_router(summarizer.router, prefix="/summarize")
app.include_router(process_url.router, prefix="/process_url")