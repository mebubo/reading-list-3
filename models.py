from datetime import datetime
from pydantic import BaseModel

class PageHighlight(BaseModel):
    id: int
    highlight: str
    highlightText: str

class PageSave(BaseModel):
    id: int
    title: str
    url: str

class SavesCount(BaseModel):
    savesCount: int

class PageSavesReponse(BaseModel):
    message: str
    details: SavesCount

class Highlight(BaseModel):
    savedAt: datetime
    highlight: str
    highlightText: str

class PageHighlights(BaseModel):
    url: str
    title: str
    highlights: list[Highlight]