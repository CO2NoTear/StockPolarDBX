import requests
import datetime


class StockData:
    pass


class Crawler:
    def __init__(self, url: str) -> None:
        self.url = url

    def crawl(date: datetime) -> StockData:
        return StockData()
