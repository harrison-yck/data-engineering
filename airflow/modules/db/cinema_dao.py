from sqlalchemy import create_engine


class CinemaDAO:
    def __init__(self, database, user, password):
        _engine = create_engine(
            "mongodb:///?Server=mongodb&;Port=27017&Database=%s&User=%s&Password=%s" % (database, user, password))

    def get_movie(self):
        pass

    def insert_movie(self):
        pass

    def update_movie(self):
        pass
