import unittest
from crawler.crawler import SZSECrawler, StockData
from datetime import datetime
from pathlib import Path


class TestCrawler(unittest.TestCase):
    def testCheckCodeSZSE(self):
        self.assertTrue(SZSECrawler.checkCode("000001"), "000001检查失败")
        self.assertFalse(SZSECrawler.checkCode("000000"), "000000检查失败")

    def testDailyQuotesImplSZSE(self):
        data = SZSECrawler.crawl_implement("000001", datetime.today())
        self.assertTrue(isinstance(data, StockData))
        savePath = data.store("./saved_data/single_coded")
        self.assertNotEqual(savePath, "")
        self.assertTrue(Path(savePath).exists())

    def testDailyQuotesAllSZSE(self):
        data = SZSECrawler.crawl(datetime.today())
        savePath = data.store("./saved_data/")
        self.assertNotEqual(savePath, "")
        self.assertTrue(Path(savePath).exists())


if __name__ == "__main__":
    unittest.main()
