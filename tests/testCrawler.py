import unittest
import crawler
from crawler.crawler import SZSECrawler, StockData
from datetime import datetime, timedelta


class TestCrawler(unittest.TestCase):
    def testCheckCodeSZSE(self):
        self.assertTrue(SZSECrawler.check_code("000001"), "000001检查失败")
        self.assertFalse(SZSECrawler.check_code("000000"), "000000检查失败")

    def testDailyQuotesSZSE(self):
        self.assertTrue(
            isinstance(
                SZSECrawler().crawl_implement(
                    "000001", datetime.today() - timedelta(days=2)
                ),
                StockData,
            )
        )


if __name__ == "__main__":
    unittest.main()
