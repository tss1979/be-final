# from asyncio.log import logger
#
# from sqlalchemy.future import select
#
# from src.db.db import db_dependency
# from src.models import ShortedUrl
# from src.models.snippet import Snippet
# from src.schemas.snippet import SnippetSchema
#
#
# async def get_url_by_id(db: db_dependency, url_id: int):
#     result = await db.execute(select(ShortedUrl).filter(ShortedUrl.id == url_id))
#     return result.scalars().first()
#
#
# async def get_url_by_shorted_url(db: db_dependency, shorted_url: str):
#     result = await db.execute(select(ShortedUrl).filter(ShortedUrl.shorted_url == shorted_url))
#     return result.scalars().first()
#
#
#
# async def create_url(db: db_dependency, origin: str, shorted_url: str):
#     db_url = ShortedUrl(origin=origin, shorted_url=shorted_url)
#     db.add(db_url)
#     await db.commit()
#     await db.refresh(db_url)
#     return db_url
#
#
#
# async def delete_url(db: db_dependency, url_id: int):
#     db_url = await get_url_by_id(db, url_id)
#     if db_url:
#         await db.delete(db_url)
#         await db.commit()
#     return db_url