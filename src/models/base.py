from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
