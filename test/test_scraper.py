import time
import unittest
<<<<<<< HEAD

from zmq import NULL
import scraper.furniture_scraper as fs
=======
from scraper.furniture_scraper import FurnitureScraper
>>>>>>> 00bf08bf2ced07d4b36e7aac38124779106c5ef1


class FunitureScraperTestCase(unittest.TestCase):
    def setUp(self):
        """
        the __init__ of the test class
        """
<<<<<<< HEAD
        # self.bot = fs.FurnitureScraper('https://www.swooneditions.com/', 'chairs')
        URL = 'https://www.swooneditions.com/'
        category = 'chairs'
        furinture_categories = ['chairs',
                            'tables',
                            'lighting']
        self.furniture_scraper = fs.FurnitureScraper(URL, category)
        self.furniture_scraper.go_to_furniture_category()

=======
        self.bot = FurnitureScraper(URL, category)
        time.sleep(5)
>>>>>>> 00bf08bf2ced07d4b36e7aac38124779106c5ef1
        return super().setUp()

    def test_generate_uuid(self) -> str:
        assert type(fs.FurnitureScraper.generate_uuid(self)) is str

<<<<<<< HEAD
    def test_click_search_bar(self): 
        assert type(fs.FurnitureScraper.click_search_bar(self)) is not NULL
=======
    def test_accept_cookies(self):
        self.bot.x_out_sign_up("//div[@data-testid='om-overlays-close']")

    def test_get_chair_price(self,
                             str_price='£1,009'):
        expected_price = 1009
        actual_price = self.bot.get_chair_price(str_price)
        self.assertEqual(expected_price, actual_price)
>>>>>>> 00bf08bf2ced07d4b36e7aac38124779106c5ef1

    def tearDown(self) -> None:
        """
        tear down the setUp
        """
        return super().tearDown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
