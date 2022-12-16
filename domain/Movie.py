from datetime import time

from dataclasses import dataclass

from domain.Cinema import Cinema
from domain.MovieStatus import MovieStatus


@dataclass()
class Movie:
    _id: str
    name: str
    status: MovieStatus
    duration: time
    rating: str
    cinema: Cinema
    image: str