import unittest
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scraper.furniture_scraper import FurnitureScraper


class FunitureScraperTestCase(unittest.TestCase):
    def setUp(self,
              URL='https://www.swooneditions.com/',
              category='chairs') -> None:
        """
        the __init__ of the test class
        """
        self.bot = FurnitureScraper(URL, category)
        self.driver = (webdriver.Chrome(service=Service(
            ChromeDriverManager().install())))

        self.driver.get(self.bot)

        return super().setUp()

    # def test_get_furniture_data():
    #    pass

    # def test_make_data_store(self, folder: str) -> None:
    #    pass

    # def test_get_furniture_images(self, name: str) -> None:
    #    pass

    def test_land_first_page(self) -> None:
        self.driver.get(self.homepage + self.category)
        pass

    def test_accept_cookies(self) -> None:
        self.bot.accept_cookies()
        pass

    def test_x_out_sign_up(self) -> None:
        self.bot.x_out_sign_up()
        pass

    def test_scroll(self, x=0, y=1000) -> None:
        pass

    def test_click_next_page(self) -> None:
        pass

    def test_click_search_bar(self) -> None:
        pass

    def test_write_data_to_file(self, folder, data) -> None:
        pass

    def test_write_images_to_file(self, image, name, number) -> None:
        pass

    def test_generate_uuid(self) -> str:
        assert type(FurnitureScraper.generate_uuid(self)) is str

    def test_upload_image_to_cloud() -> str:
        """
            check if we can see the bucket that we are uploading to 
        """

    def tearDown(self) -> None:
        """
        tear down the setUp
        """
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()
