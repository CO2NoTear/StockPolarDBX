from datetime import datetime, timedelta
from crawler.crawler import Crawler, SZSECrawler, StockData
from typing import Literal
from argparse import ArgumentParser


def crawlAllHistory(ex: Literal["SZSE"], year: int = 2024) -> StockData:
    day = datetime(year, 1, 1)
    data = StockData(ex, day, None)
    if ex == "SZSE":
        crawler = SZSECrawler()
    else:
        raise NotImplementedError(f"Exchange {ex} not done yet.")
    while day.year <= year and day < datetime.today():
        data = data.update(crawler.crawl_history(day))
        day += timedelta(1)

    return data


if __name__ == "__main__":
    parser = ArgumentParser("crawler")
    parser.add_argument("-y", "--year", type=int, required=True, nargs="+")
    args = parser.parse_args()
    for year in args.year:
        data = crawlAllHistory("SZSE", year)
        data.store("./saved_data/history")
