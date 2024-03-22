import json

from kafka import KafkaProducer
from common import Movie


class CineplexProducer:
    def __init__(self, bootstrap_servers):
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )

    def publish(self, topic, movie: Movie):
        self._producer.send(
            topic,
            value=movie
        )
