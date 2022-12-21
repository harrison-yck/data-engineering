import enum

from datetime import time
from dataclasses import dataclass
from common import Cinema


class MovieStatus(enum.Enum):
    NA = -1
    COMING_SOON = 1
    PLAYING = 2
    ENDED = 3


@dataclass(frozen=True)
class Movie:
    name: str
    status: MovieStatus
    duration: time
    rating: str
    cinema: Cinema
    image: str
