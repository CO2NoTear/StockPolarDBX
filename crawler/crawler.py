from typing import Iterator, Self, Any
import pandas as pd
import abc
from json import dump, loads
from tqdm import tqdm
import pytomlpp
import requests
from pathlib import Path
from datetime import datetime
from random import random
from dataclasses import dataclass


@dataclass
class StockData:
    ex: str
    date: datetime
    data: pd.DataFrame | None = None

    # @classmethod
    # def fromJson(cls, ex: str, date: datetime, rawJsonData: dict | None = None) -> Self:
    #     if rawJsonData is None:
    #         rawJsonData = {}
    #     newStockData = cls(ex, date, None)
    #     newStockData.data = pd.DataFrame(rawJsonData)
    #     return newStockData
    # def fromExcel(cls, ex: str, date: datetime, excelObj:Any) -> Self:

    # TODO: Broken for dailyquotes.
    # Dailylquotes does not support DataFrame
    def update(self, newData: Self) -> Self:
        if self.data is None:
            self.data = newData.data
            return self
        if newData is None or newData.data is None:
            return self
        self.data = pd.concat([self.data, newData.data], ignore_index=True)
        return self

    def store(self, saveDir: str | Path) -> str | Path:
        if self.data is None:
            return ""
        savePath = Path(
            f"{saveDir}/{self.ex.upper()}/{self.date.strftime('%Y%m%d')}.csv"
        )
        savePath.parent.mkdir(parents=True, exist_ok=True)
        fp = open(savePath, "w", encoding="utf-8")
        try:
            # dump(self.data, fp, ensure_ascii=False)
            self.data.to_csv(fp)
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

    # WARN: BROKEN
    @classmethod
    def crawl_dailyquotes(cls, date: datetime) -> StockData:
        ex = cls.getEX()
        data = StockData(ex, date)
        codeIter = cls.codeIterator()
        for code in codeIter:
            data = data.update(cls.crawl_dailyquotes_implement(code, date))
        return data

    @classmethod
    def crawl_history(cls, date: datetime) -> StockData:
        ex = cls.getEX()
        data = StockData(ex, date)
        data = cls.crawl_history_implement(date)
        return data

    @classmethod
    @abc.abstractmethod
    def crawl_dailyquotes_implement(cls, code: str, date: datetime) -> StockData:
        pass

    @classmethod
    @abc.abstractmethod
    def crawl_history_implement(cls, date: datetime) -> StockData:
        pass


class SZSECrawler(Crawler):
    DAILY_QUOTES_URL = "https://www.szse.cn/api/market/ssjjhq/getTimeData"
    STOCK_CODE_CHECK_URL = "https://www.szse.cn/api/report/shortname/gethangqing"
    HISTORY_URL = "https://www.szse.cn/api/report/ShowReport"
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
    def crawl_dailyquotes_implement(cls, code: str, date: datetime) -> StockData:
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
        return StockData(ex=cls.EX, date=date, data=pd.DataFrame({code: data}))

    @classmethod
    def crawl_history_implement(cls, date: datetime) -> StockData:
        payload = {
            "SHOWTYPE": "xlsx",
            "CATALOGID": "1815_stock_snapshot",
            "TABKEY": "tab1",
            "txtBeginDate": date.strftime("%Y-%m-%d"),
            "txtEndDate": date.strftime("%Y-%m-%d"),
            "archiveDate": "2023-01-03",
        } | cls.BASE_PAYLOAD
        resp = requests.get(url=cls.prepareURL(cls.HISTORY_URL, payload), data=payload)
        data = pd.read_excel(resp.content)
        data["成交量(万股)"] = (
            data["成交量(万股)"].str.replace(",", "").astype("Float64")
        )
        data["成交金额(万元)"] = (
            data["成交金额(万元)"].str.replace(",", "").astype("Float64")
        )
        data["市盈率"] = data["市盈率"].str.replace(",", "").astype("Float64")

        return StockData(cls.EX, date, data)
