from sqlalchemy import create_engine

from airflow.modules.db.movie import movies
from airflow.tool.redis_client import RedisClient


class CinemaDAO:
    def __init__(self, database, user, password, redis_config):
        self._engine = create_engine(
            "mongodb:///?Server=mongodb&;Port=27017&Database=%s&User=%s&Password=%s" % (database, user, password))

        self._redis = RedisClient(redis_config)

    def get_movie_status(self, cinema, movie_name):
        movie_key = self.movie_key(cinema, movie_name)
        redis_response = self._redis.get(movie_key)

        if redis_response is not None:
            return redis_response
        else:
            movie = self.get_movie_from_db(cinema, movie_name)

            if movie is not None:
                self._redis.set(movie_key, movie.status)
                return movie.status

            return None

    @staticmethod
    def get_movie_from_db(cinema, movie_name):
        return movies.select().where(movies.c.cinema == cinema and movies.c.name == movie_name)

    @staticmethod
    def movie_key(cinema, movie_name):
        return cinema.captialize() + "_" + movie_name.captialize()

    @staticmethod
    def insert_movie(movie):
        return movies.insert(movie)

    @staticmethod
    def update_movie(movie):
        return movies.update().where(movies.c.name == movie.name and movies.c.cinema == movie.cinema)\
            .values(status=movie.status)
