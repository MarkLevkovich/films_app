from db.db import Base
from sqlalchemy import Column, Integer, String


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    author = Column(String(50))