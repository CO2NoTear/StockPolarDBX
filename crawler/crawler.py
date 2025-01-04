from typing import Iterator, Self
import requests
from datetime import datetime
from random import paretovariate, random


class StockData:
    # TODO: A lot to do
    def __init__(self, rawJsonData: dict | None = None) -> None:
        print(rawJsonData)
        self.data = rawJsonData
        pass

    def update(self, newData: Self) -> Self:
        return self

    pass


class Crawler:
    EXCHANGE_LIST = ["SZSE", "SSE"]

    @classmethod
    def codeIterator(cls) -> Iterator:
        raise NotImplementedError

    @staticmethod
    def prepareURL(bareURL: str, parameters: dict[str, str]) -> str:
        req = requests.PreparedRequest()
        req.prepare_url(bareURL, parameters)
        if req.url is None:
            raise ValueError("Unable to prepare parameter for SZSE url!")
        print(req.url)
        return req.url

    def crawl(self, date: datetime) -> StockData:
        data = StockData()
        codeIter = self.codeIterator()
        for code in codeIter:
            data.update(self.crawl_implement(code, date))
        return data

    @classmethod
    def crawl_implement(cls, code: str, date: datetime) -> StockData:
        raise NotImplementedError


class SZSECrawler(Crawler):
    DAILY_QUOTES_URL = "https://www.szse.cn/api/market/ssjjhq/getTimeData"
    STOCK_CODE_CHECK_URL = "https://www.szse.cn/api/report/shortname/gethangqing"
    # HEADER = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "accept-encoding": "gzip, deflate, br, zstd",
    #     "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    #     "content-type": "application/json",
    #     "DNT": "1",
    #     "host": "www.szse.cn",
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # }
    BASE_PAYLOAD = {"random": str(random())}

    @classmethod
    def check_code(cls, code: str):
        payload = cls.BASE_PAYLOAD | {
            "dataType": "ZA||XA||DM||BG||CY||EB||JJ||ZQ||[zslb]||[qqzs]||[zczczq]||[reits]",
            "input": code,
        }
        resp = requests.get(
            url=cls.prepareURL(
                cls.STOCK_CODE_CHECK_URL,
                payload,
            ),
            data=payload,
            # headers=cls.HEADER,
        )
        try:
            if "code" in resp.json()["data"][0]:
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def crawl_implement(cls, code: str, date: datetime) -> StockData:
        # TODO: implementation
        payload = cls.BASE_PAYLOAD | {"marketId": "1", "code": "000001"}
        resp = requests.get(
            url=cls.prepareURL(cls.DAILY_QUOTES_URL, payload),
            data=payload,
            # headers=cls.HEADER,
        )
        data = {}
        try:
            data = resp.json()
            if not isinstance(data, dict):
                raise ValueError(
                    "Unable to parse json: SZSE DailyQuotes:\n" + resp.text
                )
            data.update({"date": date.strftime("%Y%M%d")})
        except:
            raise ValueError("Unable to parse json: SZSE DailyQuotes:\n" + resp.text)
        return StockData(data)
