from datetime import datetime

from selenium import webdriver

from sites import Rozetka


class Parser():


	def __init__(self, url: str):
		self.driver = webdriver.Chrome()
		self.driver.get(url)


	def get_current_price(self):
		"""Parse info about current price"""
		return self.driver.get_element_by_class_name(Rozetka.current_price_path).price


	def get_old_price(self):
		"""Parse info about old(without discount) price"""
		return self.driver.get_element_by_class_name(Rozetka.old_price_path).price


	def set_datetime(self):
		"""Set time of data parsing"""
		return datetime.now(microseconds=0)


	def run(self, driver):
		"""Start data parcing"""
		current = self.get_current_price()
		old = self.get_old_price()
		date = self.set_datetime()

		data = {'current_price': current, 'old_price': old, 'date': date}
		return data