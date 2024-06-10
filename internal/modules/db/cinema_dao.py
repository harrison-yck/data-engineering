from sqlalchemy import create_engine
from internal.modules.db.movie import movies
from internal.tool.redis_client import RedisClient
from internal.modules.db.es import ElasticSearchClient


class CinemaDAO:
    def __init__(self):
        self._engine = create_engine(
            "mongodb:///?Server=mongodb&;Port=27017&Database=%s&User=%s&Password=%s" % ('movie', 'admin', 'test123'))
        self._redis = RedisClient({'host': 'localhost', 'port': 6379})
        self._es = ElasticSearchClient({'http://elasticsearch', 9200})

    def get_movie_status(self, cinema, movie_name):
        movie_key = self.movie_key(cinema, movie_name)
        redis_response = self._redis.get(movie_key)

        if redis_response is not None:
            return redis_response
        else:
            movie_from_db = self.get_movie_by_cinema_movie_name(cinema, movie_name)

            if movie_from_db is not None:
                movie = movie_from_db.one()
                self._redis.set(movie_key, movie.status)
                return movie.status

            return None

    def search_movie(self, movie_name, cinema, status):
        return self._es.search(movie_name, cinema, status)

    def get_movie_by_cinema_movie_name(self, cinema, movie_name):
        return self._engine.execute(movies.select().where(movies.c.cinema == cinema and movies.c.name == movie_name))

    def get_movie(self, movie_id):
        return self._engine.execute(movies.select().where(movies.c.id == movie_id))

    @staticmethod
    def movie_key(cinema, movie_name):
        return cinema.captialize() + "_" + movie_name.captialize()

    def insert_movie(self, movie):
        return self._engine.execute(movies.insert(movie))

    def update_movie(self, movie):
        return self._engine.execute(movies.update()
                                    .where(movies.c.name == movie.name and movies.c.cinema == movie.cinema)
                                    .values(status=movie.status))
