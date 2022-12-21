import datetime as dt
from unittest.mock import patch

from airflow.modules.cineplex.cineplex_executor import CineplexExecutor
from airflow.modules.tests.test_tool import read_file_as_json
from common import Movie, MovieStatus, Cinema


def test_duration():
    result = CineplexExecutor.duration('3h 20m')
    expected = dt.time(3, 20)
    assert result == expected


@patch("airflow.modules.cineplex.cineplex_executor.CineplexProducer")
def test_to_movies(self):
    executor = CineplexExecutor()
    result = list(executor.to_movies(read_file_as_json("test_data/cineplex_api.txt")))

    expected = Movie(
        'Avatar: The Way of Water',
        MovieStatus.PLAYING,
        dt.time(3, 12),
        'PG',
        Cinema.CINEPLEX,
        'https://mediafiles.cineplex.com/Central/Film/Posters/27407_320_470.jpg'
    )

    assert result[0] == expected
