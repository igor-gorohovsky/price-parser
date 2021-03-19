from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from sites import Rozetka


class Parser():


	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		self.driver = webdriver.Chrome(options=options)


	def get_price(self, class_name: str) -> int:
		"""Get price by class name"""
		try:
			return self.driver.find_element_by_class_name(class_name).price
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

		data = {'current_price': current, 'old_price': old, 'date': date, 'status': status}
		return data


	def turn_off(self):
		self.driver.quit()