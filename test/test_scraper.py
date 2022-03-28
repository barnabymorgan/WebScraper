import time
import unittest
from scraper.furniture_scraper import FurnitureScraper


class FunitureScraperTestCase(unittest.TestCase):
    def setUp(self,
              URL='https://www.swooneditions.com/',
              category='chairs') -> None:
        """
        the __init__ of the test class
        """
        self.bot = FurnitureScraper(URL, category)
        time.sleep(5)
        return super().setUp()

    def test_generate_uuid(self) -> str:
        assert type(FurnitureScraper.generate_uuid(self)) is str

    def test_accept_cookies(self):
        self.bot.x_out_sign_up("//div[@data-testid='om-overlays-close']")

    def test_get_chair_price(self,
                             str_price='£1,009'):
        expected_price = 1009
        actual_price = self.bot.get_chair_price(str_price)
        self.assertEqual(expected_price, actual_price)

    def tearDown(self) -> None:
        """
        tear down the setUp
        """
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()
