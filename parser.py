from datetime import datetime
import atexit

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from sites import Rozetka


class Parser():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

        atexit.register(self.turn_off)

    def get_price(self, element_path: str) -> int:
        """ Get price by element_path.
            element_path is from class Rozetka."""
        try:
            return self.driver.find_element_by_class_name(element_path).price
        except NoSuchElementException:
            return None

    def set_datetime(self) -> datetime:
        """Set time of data parsing"""
        return datetime.now().replace(microsecond=0)

    def get_status(self, class_name):
        """Get availability status"""
        try:
            return self.driver.find_element_by_class_name(class_name).text
        except NoSuchElementException:
            raise Exception("Couldn't find a product status, check page")

    def run(self, url: str) -> dict:
        """Start data parcing"""

        self.driver.get(url)

        current = self.get_price(Rozetka.current_price_path)
        old = self.get_price(Rozetka.old_price_path)
        date = self.set_datetime()
        status = self.get_status(Rozetka.status_path)

        data = {
            'current_price': current,
            'old_price': old,
            'date': date,
            'status': status
        }
        return data

    def turn_off(self):
        self.driver.quit()
