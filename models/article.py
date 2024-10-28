#models/article.py

from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    date: str
    timestamp: str
    link: str
