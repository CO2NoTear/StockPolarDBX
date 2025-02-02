from datetime import datetime, timedelta
from crawler.crawler import Crawler, SZSECrawler, StockData
from typing import Literal


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
    data = crawlAllHistory("SZSE", 2025)
    data.store("./saved_data/history")
