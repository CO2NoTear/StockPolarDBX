import unittest
from crawler.crawler import SZSECrawler, StockData
from datetime import datetime
from pathlib import Path


class testDailyQuotesCrawler(unittest.TestCase):
    def testCheckCodeSZSE(self):
        self.assertTrue(SZSECrawler.checkCode("000001"), "000001检查失败")
        self.assertFalse(SZSECrawler.checkCode("000000"), "000000检查失败")

    def testDailyQuotesImplSZSE(self):
        data = SZSECrawler.crawl_dailyquotes_implement("000001", datetime.today())
        self.assertTrue(isinstance(data, StockData))
        savePath = data.store("./saved_data/single_coded")
        self.assertNotEqual(savePath, "")
        self.assertTrue(Path(savePath).exists())

    # def testDailyQuotesAllSZSE(self):
    #     data = SZSECrawler.crawl(datetime.today())
    #     savePath = data.store("./saved_data/")
    #     self.assertNotEqual(savePath, "")
    #     self.assertTrue(Path(savePath).exists())


class testHistoryCrawler(unittest.TestCase):
    def testDailyQuotesImplSZSE(self):
        test_date = datetime(2025, 1, 27)
        data = SZSECrawler.crawl_history_implement(test_date)
        self.assertTrue(isinstance(data, StockData))
        savePath = data.store("./saved_data/history")
        self.assertNotEqual(savePath, "")
        self.assertTrue(Path(savePath).exists())


if __name__ == "__main__":
    unittest.main()
