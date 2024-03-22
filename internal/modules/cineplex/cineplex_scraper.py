import logging
from contextlib import closing
from requests import get

from internal.tool import Retry


class CineplexScraper:
    def __init__(self, url):
        self._lang = 'en-us'
        logging.log(logging.INFO, 'Cineplex Scraper init with url: ', url)
        self.url = url

    @Retry(3)
    def get_text(self, skip: 0, size: 100):
        try:
            payload = self.get_payload(skip, size)
            with closing(get(self.url, payload)) as response:
                if response.ok:
                    return response.text
        except Exception as err:
            logging.error('fail to extract json', err)

    def get_payload(self, skip, size):
        return {"language": self._lang, "skip": skip, "take": size}
