from typing import Iterator, Self, Any
import abc
from json import dump, loads
from tqdm import tqdm
import pytomlpp
import requests
from pathlib import Path
from datetime import datetime
from random import random


class StockData:
    # TODO: A lot to do
    def __init__(
        self, ex: str, date: datetime, rawJsonData: dict | None = None
    ) -> None:
        self.data = rawJsonData
        self.date = date
        self.ex = ex
        pass

    def update(self, newData: Self) -> Self:
        if self.data is None:
            self.data = newData.data
            return self
        if newData.data is None:
            return self
        self.data |= newData.data
        return self

    def store(self, saveDir: str | Path) -> str | Path:
        if self.data is None:
            return ""
        savePath = Path(
            f"{saveDir}_{self.ex.upper()}_{self.date.strftime('%Y%m%d')}.json"
        )
        savePath.parent.mkdir(parents=True, exist_ok=True)
        fp = open(savePath, "w", encoding="utf-8")
        try:
            dump(self.data, fp, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Cannot save data to {savePath}") from e
        finally:
            fp.close()
        return savePath


class Crawler(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def getEX(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def codeIterator(cls) -> tqdm:
        pass

    @staticmethod
    def prepareURL(bareURL: str, parameters: dict[str, str]) -> str:
        req = requests.PreparedRequest()
        req.prepare_url(bareURL, parameters)
        if req.url is None:
            raise ValueError("Unable to prepare parameter for SZSE url!")
        return req.url

    @classmethod
    def crawl(cls, date: datetime) -> StockData:
        ex = cls.getEX()
        data = StockData(ex, date)
        codeIter = cls.codeIterator()
        for code in codeIter:
            data = data.update(cls.crawl_implement(code, date))
        return data

    @classmethod
    @abc.abstractmethod
    def crawl_implement(cls, code: str, date: datetime) -> StockData:
        pass


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
    EX = "SZSE"
    CODE_LISTS = pytomlpp.load("config/codeLists.toml")["codeLists"]

    @classmethod
    def getEX(cls) -> str:
        return cls.EX

    @classmethod
    def codeIterator(cls) -> tqdm:
        return tqdm(cls.CODE_LISTS)
        # for code in cls.CODE_LISTS:
        #     if cls.checkCode(code):
        #         yield code

    @classmethod
    def checkCode(cls, code: str):
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
            data = loads(
                resp.text,
            )
            if not isinstance(data, dict):
                raise ValueError(
                    "Unable to parse json: SZSE DailyQuotes:\n" + resp.text
                )
        except:
            raise ValueError("Unable to parse json: SZSE DailyQuotes:\n" + resp.text)
        return StockData(ex=cls.EX, date=date, rawJsonData={code: data})
