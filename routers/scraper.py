#routers/scraper.py

from fastapi import APIRouter, HTTPException
from services.scraper_service import collect_articles
from models.article import Article

router = APIRouter()

@router.get("/scrape", response_model=list[Article])
async def scrape_articles():
    try:
        articles = await collect_articles()
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        return sorted(articles, key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while scraping: {str(e)}")
