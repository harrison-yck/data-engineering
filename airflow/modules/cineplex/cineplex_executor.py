import json
import logging
import uuid

import datetime as dt
from airflow.dag.dag_config import Config
from airflow.modules.cineplex import CineplexScraper
from airflow.tool.redis_client import RedisClient
from domain.Cinema import Cinema
from domain.Movie import Movie
from domain.MovieStatus import MovieStatus


class CineplexExecutor:
    _total_movie_key = 'CINEPLEX_TOTAL_MOVIE'

    def __init__(self, max_workers, redis_key, redis_config):
        self.max_workers = max_workers
        self.redis_client = RedisClient(redis_key, redis_config)
        self.scraper = CineplexScraper(Config.CINEMA_API[Cinema.CINEPLEX])

    # TODO: retry
    def execute(self):
        total_movie_count = self.get_total_movie()

        response = self.scraper.get_text(0, total_movie_count)
        response_json = json.loads(response)

        self.redis_update_total_movie(response_json['totalCount'])
        self.to_movies(response_json)

    # get total movie count from redis
    # if it is empty, pull it from API and store it
    def get_total_movie(self):
        try:
            total_count_from_redis = self.redis_get_total_movie()

            if total_count_from_redis is None:
                total_count_from_api = json.loads(self.scraper.get_text(0, 0))['totalCount']
                self.redis_update_total_movie(total_count_from_api)
                return total_count_from_api

            return total_count_from_redis
        except Exception as err:
            logging.error('[Cineplex] fail to get total movie', err)

    def redis_get_total_movie(self):
        return self.redis_client.get(self._total_movie_key)

    def redis_update_total_movie(self, count: int):
        return self.redis_client.set(self._total_movie_key, count)

    def to_movies(self, json_string):
        for movie in json_string['data']:
            yield self.to_movie(movie)

    def to_movie(self, entry):
        return Movie(
            str(uuid.uuid4()),
            entry.name,
            self.movie_status(entry.isComingSoon, entry.isNowPlaying),
            self.duration(entry.duration),
            entry.mpaaRating.ratingTitle,
            Cinema.CINEPLEX,
            entry.largePosterImageUrl
         )

    def movie_status(self, isComingSoon: bool, isNowPlaying: bool):
        if isComingSoon:
            return MovieStatus.COMING_SOON
        elif isNowPlaying:
            return MovieStatus.PLAYING
        else:
            return MovieStatus.ENDED

    def duration(self, str):
        return dt.datetime.strptime(str, '%Hh %Mm').time()
