import datetime

from airflow.decorators import dag
from airflow.models.baseoperator import chain

from common import Cinema
from internal.dag.dag_config import Config
from internal.modules.cineplex.cineplex_executor import CineplexExecutor
from internal.modules.cineplex.cineplex_producer import CineplexProducer
from internal.modules.cineplex.cineplex_scraper import CineplexScraper


@dag(start_date=datetime.datetime(2024, 3, 22), schedule="@daily")
def create_dag():
    cineplex_pull_movie_executor = CineplexExecutor(
        CineplexScraper(Config.CINEMA_API[Cinema.CINEPLEX]),
        CineplexProducer(Config.KAFKA_SERVERS)
    )

    chain(cineplex_pull_movie_executor.execute())
