from server.routers.crawler import crawl_url
from server.routers.summarizer import summarize_text_first, summarize_text_remain

def process_url(url: str, is_first: bool = False):
    metadata, body_text, image_url = crawl_url(url)

    if is_first:
        summary = summarize_text_first(body_text)
    else:
        summary = summarize_text_remain(body_text)

    return {
        'url': url,
        'metadata': metadata,
        'summary': summary,
        'image_url': image_url
    }
