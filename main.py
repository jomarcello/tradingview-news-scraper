from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright
from typing import Dict
import logging
import json

app = FastAPI()

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

logger = setup_logging()

def get_news(pair: str) -> Dict:
    special_symbols = {
        'XAUUSD': 'GOLD'
    }
    
    symbol = special_symbols.get(pair, pair)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            
            url = f"https://www.tradingview.com/symbols/{symbol}/news/"
            logger.info(f"Navigating to {url}")
            page.goto(url)
            
            page.wait_for_selector('.news-table')
            
            first_news = page.locator('.news-table tr:first-child td.desc a')
            news_title = first_news.text_content()
            news_link = first_news.get_attribute('href')
            
            full_news_url = f"https://www.tradingview.com{news_link}"
            logger.info(f"Navigating to news article: {full_news_url}")
            page.goto(full_news_url)
            
            article = page.wait_for_selector('article')
            article_content = article.text_content()
            
            return {
                "title": news_title.strip(),
                "content": article_content.strip(),
                "url": full_news_url
            }
        except Exception as e:
            logger.error(f"Error scraping news: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            browser.close()

@app.post("/news")
async def get_trading_news(data: Dict):
    try:
        pair = data.get('instrument')
        if not pair:
            raise HTTPException(status_code=400, detail="No trading pair provided")
        
        logger.info(f"Fetching news for {pair}")
        result = get_news(pair)
        return result
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
