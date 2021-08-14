from sqlalchemy import Column, Integer, String
from .base import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)

    def __repr__(self):
        return f"<Movie(title='{self.title}')>"
