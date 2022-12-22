from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


class Cinema(declarative_base()):
    __tablename__ = "Cinema"
    id = Column(String, primary_key=True)
    name = Column(String)
