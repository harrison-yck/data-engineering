from fastapi import FastAPI
from pydantic import BaseModel

from common import MovieStatus
from internal.modules.db.cinema_dao import CinemaDAO

app = FastAPI()


class QueryMovie(BaseModel):
    name: str
    cinema: str
    status: MovieStatus


@app.get("/movies/query")
async def query_movie(query: QueryMovie):
    return CinemaDAO.search_movie(query.name, query.cinema, query.status)


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    return CinemaDAO.get_movie(movie_id)
