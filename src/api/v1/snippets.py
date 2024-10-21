from http.client import HTTPException

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select

from src.db.db import db_dependency
from src.models import Snippet, User

snippets_router = APIRouter(prefix="/snippets", tags=['snippets'])

@snippets_router.get("/snippets/")
async def get_snippets(db: db_dependency):
    snippets = await db.execute(select(Snippet))
    return snippets.scalars().all()

@snippets_router.get("/snippets/{snippet_uuid}")
async def get_snippet_by_id(db: db_dependency, snippet_uuid: str):
    result = await db.execute(select(Snippet).where(Snippet.uuid == snippet_uuid))
    return result.scalars().first()

@snippets_router.post("/create_snippet/")
async def create_snippet(db: db_dependency, title: str, code: str, current_user: User):
    db_snippet = Snippet(title=title, code=code, author_id=current_user.id)
    db.add(db_snippet)
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet

@snippets_router.put("/update_snippet/{snippet_uuid}")
async def update_snippet(snippet_uuid: str, snippet: Snippet, db: db_dependency, current_user: User = Depends):
    snippets = await db.execute(select(Snippet).where(Snippet.uuid == snippet_uuid))
    db_snippet = snippets.scalars.first()
    if db_snippet is None or db_snippet.author.id != current_user.id:
        raise HTTPException(status_code=404, default='Сниппет не найден')

    for key, value in snippet.dict().items():
        setattr(db_snippet, key, value)

    await db.commit()
    await db.refresh(db_snippet)

    return {"uuid": str(db_snippet.uuid), "message": f"Snippet updated successfully!"}

@snippets_router.delete("/snippets/{uuid}")
async def delete_snippet(db: db_dependency, uuid: str):
    db_snippet = await db.execute(select(Snippet).where(Snippet.uuid == uuid))
    if db_snippet:
        await db.delete(db_snippet)
        await db.commit()
    else:
        raise HTTPException(status_code=404, default='Сниппет не найден')

    return db_snippet.uui