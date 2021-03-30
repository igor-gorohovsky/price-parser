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

    browser: webdriver

    def __init__(self, is_headless: bool):
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)

        logging.basicConfig(level=logging.INFO)
        atexit.register(self.browser.quit)

    def _get_price(self, element_path: str) -> Optional[int]:
        """ Get price by element_path.

            element_path is the name of the tag or tag's attribute by which
            we can find the necessary information of the product on the page
            using Selenium API
        """

        # Check if we can find a price element
        try:
            price = self.browser.find_element_by_class_name(element_path).text
            # Remove all symbols except numbers
            return int(re.sub('\D', '', price))
        except NoSuchElementException:
            return None

    def _set_datetime(self) -> datetime:
        """Set time of parsing"""
        return datetime.now().replace(microsecond=0)

    def _get_status(self, status_path: str) -> Optional[str]:
        """Get availability status of the product

            element_path is the name of the tag or tag's attribute by which
            we can find the necessary information of the product on the page
            using Selenium API
        """
        try:
            return self.browser.find_element_by_class_name(status_path).text
        except NoSuchElementException:
            raise NoSuchElementException(
                "Couldn't find a product status, check page"
            )

    def _is_page_available(self, url: str):
        if self.browser.current_url != url:
            raise Exception("Page isn't available")

    def parse(self, urls: Dict[int, str]) -> List[Prices]:
        """Parse data"""
        data = list()

        for id, url in urls.items():
            self.browser.get(url)
            self._is_page_available(url)

            logging.info(f'Starting to parse: {url}')

            current_price = self._get_price(Rozetka.current_price_path)
            old_price = self._get_price(Rozetka.old_price_path)
            date = self._set_datetime()
            discount = old_price - current_price if old_price else None
            status = self._get_status(Rozetka.status_path)

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

    parser: Parser
    session: session.Session

    def __init__(self, is_headless: bool = True):
        self.parser = Parser(is_headless)
        Session = sessionmaker(
            bind=engine_from_config(config, prefix='db.')
        )
        self.session = Session()
        atexit.register(self.session.commit)

    def _get_urls(self):
        urls = self.session.query(Urls).all()
        return {url.id: url.url for url in urls}

    def run(self):
        urls = self._get_urls()
        data = self.parser.parse(urls)
        self.session.add_all(data)
