from datetime import datetime, timedelta
from crawler.crawler import Crawler, SZSECrawler, StockData
from typing import Literal
from argparse import ArgumentParser
from consts import ROOT_DIR


def crawlAllHistory(ex: Literal["SZSE"], year: int = 2024) -> None:
    day = datetime(year, 1, 1)
    if ex == "SZSE":
        crawler = SZSECrawler()
    else:
        raise NotImplementedError(f"Exchange {ex} not done yet.")
    while day.year <= year and day < datetime.today():
        data = crawler.crawl_history(day)
        if data.data is not None and not data.data.empty:
            data.store(ROOT_DIR + "/saved_data/history")
        day += timedelta(1)


if __name__ == "__main__":
    parser = ArgumentParser("crawler")
    parser.add_argument("-y", "--year", type=int, required=True, nargs="+")
    args = parser.parse_args()
    for year in args.year:
        crawlAllHistory("SZSE", year)
        # data.store("./saved_data/history")
