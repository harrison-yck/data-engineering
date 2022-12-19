import json
import logging

import datetime as dt
from airflow.dag.dag_config import Config
from airflow.modules.cineplex.cineplex_producer import CineplexProducer
from airflow.modules.cineplex.cineplex_scraper import CineplexScraper

from airflow.tool.redis_client import RedisClient
from common import KafkaTopic, Cinema, Movie, MovieStatus


class CineplexExecutor:
    _total_movie_key = 'CINEPLEX_TOTAL_MOVIE'

    def __init__(self, redis_key, redis_config):
        self.redis_client = RedisClient(redis_key, redis_config)
        self.scraper = CineplexScraper(Config.CINEMA_API[Cinema.CINEPLEX])
        self.producer = CineplexProducer(Config.KAFKA_SERVERS)

    # TODO: retry
    def execute(self):
        total_movie_count = self.get_total_movie()

        response = self.scraper.get_text(0, total_movie_count)
        response_json = json.loads(response)

        self.redis_update_total_movie(response_json['totalCount'])

        for movie in self.to_movies(response_json):
            self.producer.publish(KafkaTopic.movie, movie)

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

    # convert into movie and movie status and publish them
    def to_movies(self, json_string):
        for movie in json_string['data']:
            yield self.to_movie(movie)

    def to_movie(self, entry):
        return Movie(
            entry['name'],
            self.movie_status(entry['isComingSoon'], entry['isNowPlaying']),
            self.duration(entry['duration']),
            self.rating(entry['mpaaRating']['ratingTitle']),
            Cinema.CINEPLEX,
            entry['mediumPosterImageUrl']
        )

    @staticmethod
    def rating(rating):
        if rating is 'N/A' or rating is 'null':
            return None
        else:
            return rating

    @staticmethod
    def movie_status(is_coming_soon: bool, is_now_playing: bool):
        if is_coming_soon:
            return MovieStatus.COMING_SOON
        elif is_now_playing:
            return MovieStatus.PLAYING
        else:
            return None

    @staticmethod
    def duration(s):
        return dt.datetime.strptime(s, '%Hh %Mm').time()
