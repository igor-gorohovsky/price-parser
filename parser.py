from datetime import datetime

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


	def _get_price(self):
		try:
			price = self.webdriver.find_element_by_class_name(Rozetka.price_path).text
			return price
		except NoSuchElementException as e:
			print("Can't find a price")


	def start(self):
		urls = self.session.query(Urls)

		for url in urls:
			self.webdriver.get(url.url)

			price = self._get_price()
			self.session.add(Prices(url_id=url.id, date=datetime.now(), price=price))


	def save_session(self):
		self.session.commit()