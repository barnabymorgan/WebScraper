import unittest

from zmq import NULL
import scraper.furniture_scraper as fs


class FunitureScraperTestCase(unittest.TestCase):
    def setUp(self):
        """
        the __init__ of the test class
        """
        # self.bot = fs.FurnitureScraper('https://www.swooneditions.com/', 'chairs')
        URL = 'https://www.swooneditions.com/'
        category = 'chairs'
        furinture_categories = ['chairs',
                            'tables',
                            'lighting']
        self.furniture_scraper = fs.FurnitureScraper(URL, category)
        self.furniture_scraper.go_to_furniture_category()

        return super().setUp()

    def test_generate_uuid(self) -> str:
        assert type(fs.FurnitureScraper.generate_uuid(self)) is str

    def test_click_search_bar(self): 
        assert type(fs.FurnitureScraper.click_search_bar(self)) is not NULL

    def tearDown(self) -> None:
        """
        tear down the setUp
        """
        return super().tearDown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
