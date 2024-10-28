#main.py

from fastapi import FastAPI
from routers import scraper
from config import config
#from services.mongodb_service import db_service  # Import MongoDB service to close connection


app = FastAPI()

app.include_router(scraper.router, prefix="/api/v1/scraper", tags=["Cointelegraph-Scraper"])


# # MongoDB connection closure on application shutdown
# @app.on_event("shutdown")
# async def shutdown_event():
#     await db_service.client.close()  # Close MongoDB connection

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT, log_level=config.LOG_LEVEL)
