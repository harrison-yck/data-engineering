import enum

from sqlalchemy import Column, String, Integer, Time, Enum, MetaData, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.testing.schema import Table

Base = declarative_base()
meta = MetaData()


class MovieStatus(enum.Enum):
    NA = "N/A"
    COMING_SOON = "Coming Soon"
    PLAYING = "Playing"
    ENDED = "Ended"


movies = Table(
    'movie', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('cinema', String),
    Column('duration', Time),
    Column('rating', String),
    Column('image', String),
    Column('status', Enum(MovieStatus)),
    UniqueConstraint('name', 'cinema')
)
