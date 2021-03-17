from datetime import datetime
from re import sub

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.common.exceptions import *

from models.site_models import *
from sites import *


class Parser():


	def __init__(self):
		self.webdriver = webdriver.Chrome()
		Session = sessionmaker(bind=engine)
		self.session = Session()


	def _get_current_price(self):
		try:
			price = self.webdriver.find_element_by_class_name(Rozetka.current_price_path).price
			return price
		except NoSuchElementException as e:
			print("Can't find a price")


	def _get_old_price(self):
		try:
			price = self.webdriver.find_element_by_class_name(Rozetka.old_price_path).price
		except NoSuchElementException as e:
			price = None
		finally:
			return price


	def start(self):
		urls = self.session.query(Urls)

		for url in urls:
			self.webdriver.get(url.url)

			current_price = self._get_current_price()
			old_price = self._get_old_price()

			self.session.add(
				Prices(
					url_id=url.id, 
					date=datetime.now(), 
					current_price=current_price,
					old_price=old_price)
				)


	def save_session(self):
		self.session.commit()