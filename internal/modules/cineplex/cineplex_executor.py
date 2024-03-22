import json

import datetime as dt
import uuid

from common import KafkaTopic, Cinema, Movie, MovieStatus


class CineplexExecutor:
    def __init__(self, scraper, producer):
        self.scraper = scraper
        self.producer = producer

    def execute(self):
        response = self.scraper.get_text(0, 500)
        response_json = json.loads(response)

        for movie in self.to_movies(response_json):
            self.producer.publish(KafkaTopic.movie_update, movie)

    def to_movies(self, json_string):
        for movie in json_string['data']:
            yield self.to_movie(movie)

    def to_movie(self, entry):
        return Movie(
            str(uuid.uuid4()),
            entry['name'],
            self.movie_status(entry['isComingSoon'], entry['isNowPlaying']),
            self.duration(entry['duration']),
            self.rating(entry['mpaaRating']),
            Cinema.CINEPLEX,
            entry['mediumPosterImageUrl']
        )

    @staticmethod
    def rating(movie_rating):
        if movie_rating is None:
            return None

        rating = movie_rating['ratingTitle']

        if rating == 'N/A':
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
            return MovieStatus.NA

    @staticmethod
    def duration(s):
        if s == "":
            return None

        return dt.datetime.strptime(s, '%Hh %Mm').time()
