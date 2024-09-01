from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import aiosql
import aiosqlite

from models import PageHighlight, PageSavesReponse, SavesCount
import store

app = FastAPI()

DB_FILE = "db.sqlite3"

async def get_db():
    db = await aiosqlite.connect(DB_FILE)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

@app.get("/api/highlights", response_model=list[PageHighlight])
async def get_highlights(url: str, conn = Depends(get_db)):
    return await store.highlights_for_url(conn, url)

class HighlightRequest(BaseModel):
    url: str
    title: str
    highlight: str

@app.post("/api/highlights")
async def save_highlight(request: HighlightRequest, conn = Depends(get_db)):
    return await store.save_highlight(conn, request.url, request.title, request.highlight, "")

@app.get("/api/saves", response_model=PageSavesReponse)
async def get_page_saves(url: str):
    return PageSavesReponse(message=url, details=SavesCount(savesCount=5))

# serve frontend/public/standalone on /
app.mount("/", StaticFiles(directory="frontend/public/standalone", html=True))