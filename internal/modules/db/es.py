from elasticsearch import Elasticsearch
from pandas import json_normalize
import logging
import json


class ElasticSearchClient:
    def __init__(self, es_config):
        self.client = Elasticsearch([{'host': es_config.host, 'port': es_config.port}])
        self.config = es_config

        if self.client is None or not self.client.ping():
            logging.error('Unable to connect to es')

    def search(self, movie_name, cinema, status):
        es_res = self.client.search(self.config.index, json.dumps(
            {'query': {'match': {'name': movie_name, 'cinema': cinema, 'status': status}}}))
        return json_normalize(es_res['hits']['hits'])
