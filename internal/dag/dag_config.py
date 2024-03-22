from common import Cinema


class Config:
    CINEMA_API = {
        Cinema.CINEPLEX: "https://api.cineplex.com/api/v1/movies"
    }

    KAFKA_SERVERS = ["kafka:9092"]
