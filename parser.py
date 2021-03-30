from datetime import datetime
from typing import Optional, List, Dict
import atexit
import re
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, session

from sites import Rozetka
from models.site_models import Prices, Urls
from models.db_config import config


class Parser():

    __browser: webdriver

    def __init__(self, is_headless: bool):
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument('--headless')
        self.__browser = webdriver.Chrome(options=options)

        logging.basicConfig(level=logging.INFO)
        atexit.register(self.__browser.quit)

    def __get_price(self, element_path: str) -> Optional[int]:
        """ Get price by element_path.

            element_path is the name of the tag or tag's attribute by which
            we can find the necessary information of the product on the page
            using Selenium API
        """

        # Check if we can find a price element
        try:
            price = self.__browser.find_element_by_class_name(element_path).text
            return int(re.sub('\D', '', price))
        except NoSuchElementException:
            return None

    def __set_datetime(self) -> datetime:
        """Set time of parsing"""
        return datetime.now().replace(microsecond=0)

    def __get_status(self, status_path: str) -> Optional[str]:
        """Get availability status of the product

            element_path is the name of the tag or tag's attribute by which
            we can find the necessary information of the product on the page
            using Selenium API
        """
        try:
            return self.__browser.find_element_by_class_name(status_path).text
        except NoSuchElementException:
            raise NoSuchElementException(
                "Couldn't find a product status, check page"
            )

    def __connect_to_page(self, url: str):
        """Open and checks availability of the page"""
        self.__browser.get(url)
        self.__is_page_available(url)

    def __is_page_available(self, url: str):
        """Checks if we were redirected to page with captha"""
        if self.__browser.current_url != url:
            raise Exception("Page isn't available")

    def parse(self, urls: Dict[int, str]) -> List[Prices]:
        """Parse data"""
        data = list()

        for id, url in urls.items():
            self.__connect_to_page(url)

            logging.info(f'Starting to parse: {url}')

            current_price = self.__get_price(Rozetka.current_price_path)
            old_price = self.__get_price(Rozetka.old_price_path)
            date = self.__set_datetime()
            discount = old_price - current_price if old_price else None
            status = self.__get_status(Rozetka.status_path)

            data.append(
                Prices(
                    url_id=id,
                    date=date,
                    current_price=current_price,
                    old_price=old_price,
                    discount=discount,
                    status=status,
                )
            )
        return data


class Program():

    __parser: Parser
    __session: session.Session

    def __init__(self, is_headless: bool = True):
        self.__parser = Parser(is_headless)
        Session = sessionmaker(
            bind=engine_from_config(config, prefix='db.')
        )
        self.__session = Session()
        atexit.register(self.__session.commit)

    def __get_urls(self):
        """Retrieves urls from DB"""
        urls = self.__session.query(Urls).all()
        return {url.id: url.url for url in urls}

    def run(self):
        """Starts parsing and save data to DB"""
        urls = self.__get_urls()
        data = self.__parser.parse(urls)
        self.__session.add_all(data)
