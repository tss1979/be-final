import uuid
from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, UUID, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from src.models.base import Base

class Snippet(Base):
	uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=str(uuid.uuid4()))
	title = Column(String(50))
	code = Column(String(256))
	author_id = Column(Integer, ForeignKey("user_id"))
	created_at = Column(TIMESTAMP, default=datetime.now())
	author = relationship('User', back_populates="snippets")

