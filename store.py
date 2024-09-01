from datetime import datetime
import json
import aiosqlite
from pydantic import BaseModel

from models import Highlight, PageHighlight, PageHighlights

QUERY_GET_HIGHLIGHTS = """
    select h.id, h.highlight, h.highlightText from PageHighlights h join Page p on h.pageId = p.id where p.url = ?
"""

async def highlights_for_url(conn: aiosqlite.Connection, url: str) -> list[PageHighlight]:
    async with conn.execute(QUERY_GET_HIGHLIGHTS, (url,),) as cursor:
        highlights = await cursor.fetchall()
    return [PageHighlight(**dict(highlight)) for highlight in highlights]

async def save_highlight(conn: aiosqlite.Connection, url: str, title: str, highlight: str, highlight_str: str) -> int | None:
    async with conn.execute("select id from Page where url = ?", (url,)) as cursor:
        page_id = await cursor.fetchone()
    if not page_id:
        print("inserting new page")
        async with conn.execute("insert into Page (url, title) values (?, ?)", (url, title)) as cursor:
            page_id = cursor.lastrowid
            print("new page id", page_id)
    else:
        page_id = page_id["id"]
    async with conn.execute("insert into PageHighlights (pageId, highlight, highlightText) values (?, ?, ?)", (page_id, highlight, highlight_str)) as cursor:
        print ("new highlight id", cursor.lastrowid)
        result = cursor.lastrowid
    await conn.commit()
    return result


QUERY_GET_ALL_HIGHLIGHTS = """
    SELECT p.url, p.title, json_group_array(json_object(
        'id', h.id,
        'savedAt', h.savedAt,
        'highlight', h.highlight,
        'highlightText', h.highlightText
    )) as highlights
    FROM PageHighlights h
    JOIN Page p ON h.pageId = p.id
    GROUP BY p.url, p.title
"""

async def get_all_highlights(conn: aiosqlite.Connection) -> list[PageHighlights]:
    async with conn.execute(QUERY_GET_ALL_HIGHLIGHTS) as cursor:
        rows = await cursor.fetchall()

    pages = []
    for row in rows:
        url, title, highlights_json = row
        highlights = json.loads(highlights_json)
        page = PageHighlights(
            url=url,
            title=title,
            highlights=[Highlight(**highlight) for highlight in highlights]
        )
        pages.append(page)

    return pages
