import yaml
import time
import uuid
import json
import os
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
                 port_number: int = 9920,
                 headless: Optional[bool] = False,
                 creds: str = 'config/rds_creds.yaml') -> None:
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--remote-debugging-port=9222")
        self.driver = (webdriver.Chrome(service=Service(
            ChromeDriverManager().install()),
            options=self.chrome_options
            ))
        with open(creds, 'r') as f:
            creds = yaml.safe_load(f)
        self.driver.get(url)

    def __exit__(self) -> None:
        """
            __exit__(self)

            self

            used to quit the scraper when the data is collected
        """
        self.driver.quit()

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
        time.sleep(10)
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

    def scroll(self, x=0, y=1000) -> None:
        """
            scroll(self, x, y)

            self
            x: scroll in x plane
            y: scroll in y plane

        """
        try:
            self.driver.execute_script(f'window.scrollBy({x}, {y})')
        except NotImplementedError:
            print("Could not scroll")

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
                         xpath) -> None:
        """
            click_search_bar(self)

            self
            xpath: XPATH string used to find the search bar element

            used to click on the search bar
        """
        try:
            self.search_bar = (
                WebDriverWait(self.driver, 5)
                .until(EC.presence_of_all_elements_located(
                    (By.XPATH, xpath))
                    )
                )
            self.search_bar.click()
            return self.search_bar
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
        search_bar = self.click_search_bar()
        if search_bar:
            search_bar.send_keys(word)
            search_bar.send_keys(Keys.ENTER)
        else:
            raise Exception("Could not send keys to search bar")

    def find_container(self, xpath) -> None:
        """
            find_container()

            self
            xpath

            find the container that holds the data
            we then cycle through this to get the return the images
        """
        return self.driver.find_element()


class FurnitureScraper(Scraper):
    """
    This class is a scraper that can be used to scrape websites

    homepage (url): link to webpage we want to visit
    category: section of the website

    driver:
        this is the webdriver object
    """
    def __init__(self,
                 homepage: str = 'https://www.swooneditions.com/',
                 category: list = []):
        """
            __init__(self, homepage, category)

            self
            homepage: url of webpage we're connecting to
            category: category within that page
            port_number:
            headless:
            verbose:

            used to initialse the scaraper
        """
        super().__init__()
        self.furniture_data = {
            "uuid": [],
            "chair_category": [],
            "chair_name": [],
            "chair_price": [],
            "chair_type": []
        }
        self.image_data = {
            "uuid": [],
            "property_uuid": [],
            "image_link": []
        }
        self.category = category
        # df = pd.read_sql('properties_2', self.engine)
        # self.friendly_id_scraped = list(df['Friendly_ID'])

    def go_to_furniture_category(self) -> None:
        self.accept_cookies()
        self.send_keys_to_search_bar()
        pass

    def get_links(self,
                  container,
                  href_xpath: str = "") -> list:

        list_elements = container.find_elements(By.XPATH, )
        href_list = []

        for element in list_elements:
            href = (element.find_element(By.XPATH, href_xpath)
                    .get_attribute('href'))
            href_list.append(href)

        return href_list

    def get_furniture_data(self) -> None:
        """
            get_furniture_data(self)

            self

            used to gather the furniture data
            text-based and image data is collected from this function
        """
        self.category_container = (self.driver.find_element(
                By.XPATH, "//div[@class='items-items-3Yc']"))
        self.category_list = (self.category_container.find_elements(
                By.XPATH,
                './div'))

        for i in tqdm(range(400)):

            # TODO
            # 1. If item has already been searched
            #       skip
            #    else
            #       get info
            # 2. Go to next page
            # 3. Go to next item

            # friendly_id = href.split('/')[-2]
            #     if friendly_id in self.friendly_id_scraped:
            #         print('Already scraped')
            #         continue
            #     else:
            # href to find name of all the chairs

            for item in range(len(self.category_list)):
                # contianer
                self.category_container = (self.driver.find_element(
                        By.XPATH,
                        "//div[@class='items-items-3Yc']"))
                self.chair = (self.category_container.find_elements(
                        By.XPATH,
                        './div')
                        [item])
                self.chair.click()
                time.sleep(5)

                try:
                    self.chair_name = (self.driver.find_element(
                            By.XPATH,
                            "//h1[@class='productFullDetail-productName-BbW']")
                            .text)
                except NoSuchElementException:
                    self.chair_name = "N/A"

                try:
                    self.chair_price = (self.driver.find_element(
                        By.XPATH,
                        "//span[@class='productFullDetail-current-2sG']")
                        .text)
                except NoSuchElementException:
                    self.chair_price = "N/A"
                # remove the first char (£) so we can store a float
                self.chair_price = self.get_chair_price(self.chair_price)

                try:
                    self.chair_type = (self.driver.find_element(
                        By.XPATH,
                        "//div[@class='productFullDetail-productSubtitle-3aT']"
                                                            ).text)
                except NoSuchElementException:
                    self.chair_type = "N/A"

                self.make_data_store(
                        f"../raw_data/{self.chair_name}")
                self.chair_uuid = self.generate_uuid()
                self.chair_dict = self.get_furniture_images(self.chair_name)

                self.furniture_data['uuid'].append(self.chair_uuid)
                self.furniture_data['chair_name'].append(self.chair_name)
                self.furniture_data['chair_price'].append(self.chair_price)
                self.furniture_data['chair_type'].append(self.chair_type)
                self.furniture_data['chair_images'].append(self.chair_dict)

                self.chair_data = {
                    "uuid": self.data['uuid'][item],
                    "chair_name": self.data['chair_name'][item],
                    "chair_price": self.data['chair_price'][item],
                    "chair_type": self.data['chair_type'][item],
                    "chair_images": self.data['chair_images'][item]
                }

                self.write_data_to_file(
                        f"../raw_data/{self.chair_name}", self.chair_data)
                self.driver.back()
                time.sleep(2)

            self.click_next_page()

    def get_chair_price(self, str_price: str) -> int:
        str_price = str_price[1:].replace(',', '')
        chair_price = float(str_price)
        return chair_price

    def make_data_store(self, folder: str) -> None:
        """
            make_data_store(self, foler: str)

            folder
        """
        if not os.path.exists(folder):
            print("making folder ", folder)
            os.makedirs(folder)
            if folder != "../raw_data":
                os.makedirs(folder + "/Images")

    def find_container(self,
                       xpath: str = None) -> None:
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
        try:
            # container
            self.photo_reel = (self.driver.find_element(
                    By.XPATH, '//div[@class="cylindo-viewer-container"]'))
            self.photo_reel_list = (self.photo_reel.find_elements(
                    By.XPATH, './ul/li/img'))
            print(len(self.photo_reel_list))

            for image in range(1, len(self.photo_reel_list)):
                print("looking for image")
                self.photo = (self.driver.find_element(
                        By.XPATH,
                        f'//*[@id="cylindoViewerWrapper"]\
                            /div[2]/ul/li[{image}]/img').
                        get_attribute("src"))
                self.write_images_to_file(self.photo, name, image)

                self.uuid = self.generate_uuid()
                self.image_number = image
                self.furniture_uuid = furniture_uuid
                self.image_url = self.photo

                (self.image_data['image_data']['uuid']
                    .append(self.uuid))
                (self.image_data['image_data']['image_number']
                    .append(self.image_number))
                (self.image_data['image_data']['image_number']
                    .append(self.image_number))
                (self.image_data['image_data']['image_url']
                    .append(self.image_url))

            return self.image_data

        except NotImplementedError:
            # other method of finding images
            # container
            self.photo_container = self.driver.find_element(
                By.XPATH,
                "//div[@class='ProductGallery-galleryMain-3dh']")
            self.photo_list = self.photo_container.find_elements(
                    By.XPATH, './picture')
            print(len(self.photo_list))

            try:
                print(f"Looking for image {image}")
                print("1st try")
                self.photo = self.driver.find_element(
                    By.XPATH,
                    f'//*[@id="root"]/main/div/form/section/div[1]/div[2]/\
                    picture[{image}]/img').get_attribute("src")
                self.photo_alt = self.driver.find_element(
                    By.XPATH,
                    f'//*[@id="root"]/main/div/form/section/div[1]/div[2]/\
                        picture[{image}]/img').get_attribute("alt")
                self.write_images_to_file(self.photo, name, image)
            except WebDriverException:
                print("2nd except")
                self.photo = "None"

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

    def click_next_page(self,
                        xpath: str =
                        "//a[@class='navButton-buttonArrow-1UO tile-button-mjy \
                            Link-link-2FT']") -> None:
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

    def write_data_to_file(self, folder: str, data: dict) -> None:
        """
            write_data_to_file(self, folder, data)

            self
            folder: folder to write data to
            data: json data to write

            used to write text / tabular data to file
        """
        try:
            with open(f'../raw_data/{folder}/data.json', "w") as f:
                json.dump(data, f)

        except NotImplementedError:
            print("Could not write data to file")

    def write_images_to_file(self, image: str, name: str, number: int) -> None:
        """
            write_images_to_file(self, image, name, number)

            self
            image: url link to the image
            name: name of item
            number: number of image / iteration

            used to write the images downloaded to the correct dir.
        """
        try:
            print("trying to save image")
            urllib.request.urlretrieve(
                image,
                f"../raw_data/{name}/Images/{name}_{number}.jpg")
        except NotImplementedError:
            print("Could not save image")

    def generate_uuid(self) -> str:
        """
            generate_uuid(self)

            self

            used to generate and return a uuid
        """
        return str(uuid.uuid4())


class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store
        the scraped images and features.
    '''
    def __init__(self, s3_params) -> None:
        self.bucket_name = s3_params['bucket_name']
        self.aws_access_key_id = s3_params['access_key_id']
        self.aws_secret_access_key = s3_params['secret_access_key']

    def upload_images_to_datalake(self, data) -> None:
        '''
        This function obtains both an image SRC and ID from the page_dict.json
            file. A tempory directory is constructed and
            each SRC is accesses, downloaded and then uploaded to the S3
            bucket using the ID as a file name.

            TODO: IMPORT THE PRIVATE CREDENTIALS VIA FILE FORMATE FOR SECURITY

            Returns:
                None
        '''

        image_list = []
        for key, item in data.items():
            image_list.append((key, item['SRC']))

        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        s3 = session.client('s3')
        # Create a temporary directory,
        # so you don't store images in your local machine
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, image in enumerate(tqdm(image_list)):
                # headers allow bypass of the website security restrictions
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                            AppleWebKit/537.11 (KHTML, like Gecko) \
                                Chrome/23.0.1271.64 Safari/537.11',
                           'Accept': 'text/html,application/xhtml+xml,\
                                application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                           'Accept-Encoding': 'none',
                           'Accept-Language': 'en-US,en;q=0.8',
                           'Connection': 'keep-alive'}
                id = image[0]
                src = image[1]
                request_ = urllib.request.Request(src, None, headers)
                # store the response
                response = urllib.request.urlopen(request_)
                f = open(f'{temp_dir}/image_{i}.jpg', 'wb')
                f.write(response.read())
                # s3.upload_file(f'{temp_dir}/image_{i}.jpg',
                # 'urbanoutfittersbucket', f'{id}.jpg')
                s3.upload_file(f'{temp_dir}/image_{i}.jpg',
                               self.bucket_name,
                               f'{id}.jpg')


def data_storage_credentials_from_json():
    with open('data_storage_credentials.json') as json_file:
        # with open('Urbanoutfitters-Scraper-Project/
        # data_storage_credentials.json') as json_file:
        storage_credentials = json.load(json_file)
    s3_bucket_credentials = storage_credentials['s3_bucket']
    rds_credentials = storage_credentials['rds']
    return (s3_bucket_credentials, rds_credentials)


def data_storage_credentials_from_cli():

    print('Please enter the S3 bucket credentials:')
    bucket_name = input('S3 Bucket name: ')
    access_key_id = input('Access Key ID: ')
    secret_access_key = input('Secret Access Key: ')
    s3_bucket_credentials = {'bucket_name': bucket_name,
                             'access_key_id': access_key_id,
                             'secret_access_key': secret_access_key}

    print('Please enter the RDS credentials:')
    DATABASE_TYPE = input('Database Type: ')
    DBAPI = input('DB API: ')
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


if __name__ == '__main__':
    URL = 'https://www.swooneditions.com/'
    category = 'chairs'
    furinture_categories = ['chairs',
                            'tables',
                            'lighting']
    
    furniture_scraper = FurnitureScraper(URL)
    
    
    
    
    for category in furinture_categories:

        furniture_scraper.accept_cookies()
        furniture_scraper.get_furniture_data()
