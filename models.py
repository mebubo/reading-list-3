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