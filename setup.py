from setuptools import setup
from setuptools import find_packages

setup(
    name="swoon-website-scraper",
    version="0.0.1",
    description="A webscraper for the swoon wesite",
    long_description="A package for scraping the data (tabular) and images from swooneditions.com",
    url="https://github.com/barnabymorgan/WebScraper",
    author="Barney Morgan",
    license="MIT",
    packages=find_packages(),
    install_requires=["webdriver_manager",
                      "selenium",
                      "sqlalchemy",
                      "pandas",
                      "psycopg2-binary",
                      "boto3",
                      "tqdm",
                      "urllib3"]
)
