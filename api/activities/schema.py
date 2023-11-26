from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Activities(Base):
    __tablename__ = "activities"

    id = Column(String(100), primary_key=True)
    title = Column(String(100))
    story = Column(Text)

    def __repr__(self):
        return f"<Activities(id={self.id}, title='{self.title}', story='{self.story}')>"
