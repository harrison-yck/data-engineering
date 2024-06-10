import enum

from datetime import time
from dataclasses import dataclass
from common import Cinema


class MovieStatus(enum.Enum):
    NA = "N/A"
    COMING_SOON = "Coming Soon"
    PLAYING = "Playing"
    ENDED = "Ended"


@dataclass(frozen=True)
class Movie:
    id: str
    third_party_id: str
    name: str
    status: MovieStatus
    duration: time
    rating: str
    cinema: Cinema
    image: str
