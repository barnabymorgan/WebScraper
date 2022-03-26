from sqlalchemy import create_engine
import pandas as pd
import time
import uuid
import boto3
import urllib.request
import tempfile
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Optional
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    """

    """
    def __init__(self,
                 url: str,
                 headless: Optional[bool] = False) -> None:
        chrome_options = Options()
        if headless:
            print("headless")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--window-size=1920,1080")
            # chrome_options.add_argument("--remote-debugging-port=9230")
            self.driver = (webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=chrome_options
                ))
        else:
            print("GUI")

            self.driver = (webdriver.Chrome(service=Service(
                ChromeDriverManager().install())
                ))

        self.driver.get(url)
        self.creds = self.data_storage_credentials_from_cli()
        self.creds_rds = self.creds[1]
        self.creds_s3 = self.creds[0]

        self.client = boto3.client(
            's3',
            aws_access_key_id=self.creds_s3['access_key_id'],
            aws_secret_access_key=self.creds_s3['secret_access_key']
        )
        self.engine = (create_engine(
            f"{self.creds_rds['DATABASE_TYPE']}+{self.creds_rds['DBAPI']}://{self.creds_rds['USER']}:{self.creds_rds['PASSWORD']}@{self.creds_rds['ENDPOINT']}:{self.creds_rds['PORT']}/{self.creds_rds['DATABASE']}"))
        self.engine.connect()

    def __exit__(self) -> None:
        """
            __exit__(self)

            self

            used to quit the scraper when the data is collected
        """
        self.driver.quit()

    def data_storage_credentials_from_cli(self) -> tuple:

        print('Please enter the S3 bucket credentials:')
        bucket_name = input('S3 Bucket name: ')
        access_key_id = input('Access Key ID: ')
        secret_access_key = input('Secret Access Key: ')
        access_region = input('Secret Access Key: ')
        s3_bucket_credentials = {'bucket_name': bucket_name,
                                 'access_key_id': access_key_id,
                                 'secret_access_key': secret_access_key,
                                 'access_region': access_region}

        print('Please enter the RDS credentials:')
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        ENDPOINT = input('Endpoint: ')
        USER = input('Username: ')
        PASSWORD = input('Password: ')
        PORT = input('Port: ')
        DATABASE = input('Database: ')
        rds_credentials = {
            'DATABASE_TYPE': DATABASE_TYPE,
            'DBAPI': DBAPI,
            'ENDPOINT': ENDPOINT,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'PORT': PORT,
            'DATABASE': DATABASE
        }
        return (s3_bucket_credentials, rds_credentials)

    def accept_cookies(self,
                       xpath: str) -> None:
        """
            accept_cookies(self)

            self

            used to accept the cookies on the landing page
        """
        # WebDriverWait(self.driver, 5)
        #         .until(EC.presence_of_all_elements_located(
        #             (By.XPATH, xpath))
        #             )
        #         )
        time.sleep(5)
        furniture_scraper.x_out_sign_up()
        cookies_button = self.driver.find_element(By.XPATH, xpath)
        cookies_button.click()

    def x_out_sign_up(self,
                      xpath: str) -> None:
        """
            x_out_of_sign_up(self)

            self

            used to click the x off of the email signup prompt
        """
        try:
            x_button = self.driver.find_element(By.XPATH, xpath)
            x_button.click()
        except NotImplementedError:
            print("No sign up box found")

    def click_next_page(self,
                        xpath: str) -> None:
        """
            click_next_page(self)

            self

            used to click on the next page
        """
        try:
            next_button = self.driver.find_element(By.XPATH, xpath)
            next_button.click()
        except NotImplementedError:
            print("Could not go to the next page")

    def click_search_bar(self,
                         xpath: str) -> None:
        """
            click_search_bar(self)

            self
            xpath: XPATH string used to find the search bar element

            used to click on the search bar
        """
        try:
            search_bar = self.driver.find_element(By.XPATH, xpath)
            search_bar.click()
            return search_bar
        except TimeoutException:
            print("Could not find search bar")
            return None

    def send_keys_to_search_bar(self,
                                word: str,
                                xpath: str) -> None:
        """
            send_keys_to_search_bar(self)

            self

            used to send keys (add word to search) to search bar
        """
        search_bar = self.click_search_bar(xpath)
        if search_bar:
            search_bar.send_keys(word)
            search_bar.send_keys(Keys.ENTER)
        else:
            raise Exception("Could not send keys to search bar")

    def find_container(self,
                       xpath: str) -> None:
        """
            find_container()

            self
            xpath

            find the container that holds the data
            we then cycle through this to get the return the images
        """
        return self.driver.find_element(By.XPATH, xpath)


class FurnitureScraper(Scraper):
    """
    This class is a scraper that can be used to scrape websites

    homepage (url): link to webpage we want to visit
    category: section of the website

    driver:
        this is the webdriver object
    """
    def __init__(self,
                 url: str = 'https://www.swooneditions.com/',
                 category: str = "chairs"):
        """
            __init__(self, homepage, category)

            self
            homepage: url of webpage we're connecting to
            category: category within that page

            used to initialse the scaraper
        """
        super().__init__(url,
                         headless=True)

        self.furniture_data = {
            "uuid": [],
            "furniture_category": [],
            "long_furniture_name": [],
            "furniture_name": [],
            "furniture_price": [],
            "furniture_type": []
        }
        self.image_data = {
            "uuid": [],
            "furniture_uuid": [],
            "image_url": [],
            "image_link": []
        }
        self.category = category
        df = pd.read_sql("furniture_data", self.engine)
        self.furniture_name_scraped = list(df['long_furniture_name'])

    def go_to_furniture_category(self) -> None:
        self.accept_cookies()
        self.send_keys_to_search_bar(self.category,
                                     xpath='//*[@id="search"]')
        time.sleep(3)

    def get_links(self,
                  container,
                  href_xpath: str = (
                    ".//a[@class='ProductCard-productCard-3hF Link-link-2FT']")
                  ) -> list:
        time.sleep(2)
        # list_elements = container.find_elements(By.XPATH, './div')
        number_pages = self.get_page_numbers()
        href_list = []

        for page in number_pages:
            list_elements = container.find_elements(By.XPATH, './div')

            for element in list_elements:
                href = (element.find_element(By.XPATH, href_xpath)
                        .get_attribute('href'))
                href_list.append(href)

            self.driver.get(page)
            time.sleep(3)
            container = self.driver.find_element(By.XPATH,
                                                 "//div[@class\
                                                     ='items-items-3Yc']")
        return href_list

    def get_page_numbers(self,
                         xpath: str = (
                            "//a[@class=' tile-button-mjy Link-link-2FT']")
                         ) -> int:
        time.sleep(2)
        pages_href = []
        number_pages = self.driver.find_elements(By.XPATH,
                                                 xpath)

        for page in number_pages:
            pages_href.append(page.get_attribute('href'))

        return pages_href

    def get_furniture_data(self,
                           href_list,
                           category) -> None:
        """
            get_furniture_data(self)

            self

            used to gather the furniture data
            text-based and image data is collected from this function
        """
        for href in tqdm(href_list):
            furniture_name = href.split('/')[-1]
            if furniture_name in self.furniture_name_scraped:
                print('Already scraped')
                continue
            else:
                self.driver.get(href)
                self.photo_reel = (WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//div[@class='productFullDetail-productTitle-uNY']"))
                    ))

                try:
                    self.long_furniture_name = furniture_name = href.split('/')[-1]
                except NoSuchElementException:
                    self.long_furniture_name = "N/A"
                try:
                    self.furniture_name = (self.driver.find_element(
                            By.XPATH,
                            "//h1[@class='productFullDetail-productName-BbW']")
                            .text)
                except NoSuchElementException:
                    self.furniture_name = "N/A"

                try:
                    self.furniture_price = (self.driver.find_element(
                        By.XPATH,
                        "//span[@class='productFullDetail-current-2sG']")
                        .text)
                    self.furniture_price = self.get_chair_price(self.furniture_price)
                except NoSuchElementException:
                    self.furniture_price = "N/A"
                # remove the first char (£) so we can store a float

                try:
                    self.furniture_type = (self.driver.find_element(
                        By.XPATH,
                        "//div[@class='productFullDetail-productSubtitle-3aT']"
                                                            ).text)
                except NoSuchElementException:
                    self.furniture_type = "N/A"

                self.furniture_uuid = self.generate_uuid()
                self.chair_dict = self.get_furniture_images(
                    self.furniture_name,
                    self.furniture_uuid)

                print(self.chair_dict)

                self.furniture_data['uuid'].append(self.furniture_uuid)
                self.furniture_data['furniture_category'].append(self.category)
                (self.furniture_data['long_furniture_name']
                    .append(self.long_furniture_name))
                self.furniture_data['furniture_name'].append(
                    self.furniture_name)
                self.furniture_data['furniture_price'].append(
                    self.furniture_price)
                self.furniture_data['furniture_type'].append(
                    self.furniture_type)

                furniture_df = pd.DataFrame.from_dict(self.furniture_data)
                furniture_df.to_sql("furniture_data",
                                    self.engine,
                                    if_exists='replace')

    def get_chair_price(self, str_price: str) -> int:
        str_price = str_price[1:].replace(',', '')
        chair_price = float(str_price)
        return chair_price

    def find_container(self,
                       xpath: str = "//div[@class='items-items-3Yc']") -> None:
        return super().find_container(xpath)

    def get_furniture_images(self,
                             name: str,
                             furniture_uuid: str) -> None:
        """
            get_furniture_images(self, name: str)

            self
            name: name of the piece the images are relating to

            used to pull the images of the furniture item
        """

        # check source to see if its been scraped
        self.cylindo = False
        self.gallery = False

        try:
            (self.driver.find_element(
                    By.XPATH, '//div[@class="cylindo-viewer-container"]'))
            self.cylindo = True
            print("Cyli: ", self.cylindo)
        except NoSuchElementException:
            (self.driver.find_element(
                    By.XPATH,
                    "//div[@class='ProductGallery-galleryMain-3dh']"))
            self.gallery = True
            print("Gall: ", self.gallery)
        finally:
            print("No such element")
        try:
            if self.cylindo:
                self.photo_reel = (WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='cylindo-viewer-container']"))
                    ))
                self.photo_reel_list = (self.photo_reel.find_elements(
                        By.XPATH, './ul/li/img'))

                for image in range(1, len(self.photo_reel_list)):
                    self.photo = (self.driver.find_element(
                            By.XPATH,
                            f'//*[@id="cylindoViewerWrapper"]\
                                /div[2]/ul/li[{image}]/img').
                            get_attribute("src"))

                    self.uuid = self.generate_uuid()
                    self.image_number = image
                    self.furniture_uuid = furniture_uuid
                    self.image_url = self.photo

                    self.image_data['uuid'].append(self.uuid)
                    (self.image_data['furniture_uuid']
                        .append(self.furniture_uuid))
                    self.image_data['image_link'].append(self.image_url)
                    print(self.image_data)

            if self.gallery:
                self.photo_container = (WebDriverWait(self.driver, 7).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//div[@class='ProductGallery-galleryMain-3dh']"))
                    ))
                self.photo_list = self.photo_container.find_elements(
                        By.XPATH, './picture')

                with tempfile.TemporaryDirectory() as tmpdirname:
                    for image in range(1, len(self.photo_list)):
                        self.photo = self.driver.find_element(
                            By.XPATH,
                            f'//*[@id="root"]/main/div/form/section/div[1]/div[2]/\
                            picture[{image}]/img').get_attribute("src")

                        self.photo_alt = self.driver.find_element(
                            By.XPATH,
                            f'//*[@id="root"]/main/div/form/section/div[1]/div[2]/\
                                picture[{image}]/img').get_attribute("alt")
                        self.uuid = self.generate_uuid()
                        self.image_number = image
                        self.furniture_uuid = furniture_uuid
                        self.image_url = self.photo

                        self.image_data['uuid'].append(self.uuid)
                        (self.image_data['furniture_uuid']
                            .append(self.furniture_uuid))
                        self.image_data['image_url'].append(self.image_url)

                        time.sleep(2)
                        urllib.request.urlretrieve(self.photo,
                                                   tmpdirname +
                                                   f'/{self.uuid}.jpg')
                        self.bucket_name = self.creds_s3['bucket_name']
                        self.client.upload_file(tmpdirname + f'/{self.uuid}.jpg',
                                                f'{self.bucket_name}',
                                                f'{self.uuid}.jpg')
                        self.image_data['image_link'].append(
                            f'https://{self.bucket_name}.s3.amazonaws.com/{self.uuid}.jpg')
                        image_df = pd.DataFrame.from_dict(self.image_data)
                        image_df.to_sql("image_data",
                                        self.engine,
                                        if_exists='replace')

        except NoSuchElementException:
            print("Couldn't find images")

    def accept_cookies(self,
                       xpath: str =
                       '//*[@id="root"]/div[2]/div/div[2]/button') -> None:
        """
            accept_cookies(self)

            self

            used to accept the cookies on the landing page
        """
        # WebDriverWait
        time.sleep(10)
        furniture_scraper.x_out_sign_up()
        cookies_button = self.driver.find_element(By.XPATH, xpath)
        cookies_button.click()

    def x_out_sign_up(self,
                      xpath: str =
                      "//div[@data-testid='om-overlays-close']") -> None:
        """
            x_out_of_sign_up(self)

            self

            used to click the x off of the email signup prompt
        """
        try:
            x_button = self.driver.find_element(By.XPATH, xpath)
            x_button.click()
        except NotImplementedError:
            print("No sign up box found")

    def generate_uuid(self) -> str:
        """
            generate_uuid(self)

            self

            used to generate and return a uuid
        """
        return str(uuid.uuid4())


if __name__ == '__main__':
    URL = 'https://www.swooneditions.com/'
    category = 'chairs'
    furinture_categories = ['chairs',
                            'tables',
                            'lighting']
    furniture_scraper = FurnitureScraper(URL, category)
    furniture_scraper.go_to_furniture_category()
    container = furniture_scraper.find_container()
    links = furniture_scraper.get_links(container)
    furniture_scraper.get_furniture_data(links, category)
    Scraper.__exit__()
