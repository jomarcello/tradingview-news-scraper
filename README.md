# TradingView News Scraper

A FastAPI service that scrapes the latest news for trading pairs from TradingView.

## Features

- Scrapes latest news for specific trading pairs
- Returns news title, content, and URL
- Supports special symbols (e.g., XAUUSD → GOLD)
- Built with FastAPI and Playwright
- Dockerized for easy deployment

## API Usage

POST `/news`

Request body:
```json
{
    "instrument": "XAUUSD"
}
```

Response:
```json
{
    "title": "News Title",
    "content": "Article content...",
    "url": "https://www.tradingview.com/..."
}
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run the server:
```bash
uvicorn main:app --reload
```

## Deployment

This project is set up for deployment on Railway.app through GitHub integration.
