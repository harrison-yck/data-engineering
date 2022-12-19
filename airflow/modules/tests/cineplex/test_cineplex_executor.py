import datetime as dt

from airflow.modules.cineplex.cineplex_executor import CineplexExecutor
from common import Movie, MovieStatus, Cinema
from ..fixtures import cineplex_api_response, redis_config


def test_duration():
    result = CineplexExecutor.duration('3h 20m')
    expected = dt.time(3, 20)
    assert result == expected


def test_to_movies(redis_config, cineplex_api_response):
    executor = CineplexExecutor("test", redis_config)
    result = list(executor.to_movies(cineplex_api_response))[0]

    expected = Movie(
        'Avatar: The Way of Water',
        MovieStatus.PLAYING,
        dt.time(3, 12),
        'PG',
        Cinema.CINEPLEX,
        'https://mediafiles.cineplex.com/Central/Film/Posters/27407_320_470.jpg'
    )

    assert result == expected
