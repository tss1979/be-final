from datetime import datetime

from typing_extensions import dataclass_transform

from src.models.base import Base


class SnippetSchema(Base):
    uuid: str
    title: str
    code: str
    created_at: int

    class Config:
        orm_mode = True