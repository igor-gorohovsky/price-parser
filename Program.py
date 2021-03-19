import logging

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from parser import Parser
from models.site_models import Urls, Prices
from models.db_config import config


class Program():


	def __init__(self):
		Session = sessionmaker()
		self.session = Session(bind=engine_from_config(config, prefix='db.'))
		logging.basicConfig(level=logging.INFO)


	def start(self):
		"""Parse all urls from db"""

		# Get all urls from db
		urls = self.session.query(Urls)

		parser = Parser()

		# Start parse
		for url in urls:
			logging.info(f'Starting to parse: {url.url}')
			data = parser.run(url.url)


			# If current_price was found then add data to session
			if data['current_price']:
				self.session.add(
					Prices(
						url_id=url.id, 
						date=data['date'], 
						current_price=data['current_price'],
						old_price=data['old_price'],
						discount=None if not data['old_price'] else data['old_price']-data['current_price'],
						status=data['status']
					)
				)

		logging.info('Finishing parsing...')
		parser.turn_off()

		logging.info('Saving the received data to the database...')
		self.session.commit()



	def save_session(self):
		"""Save parsing data to db"""
		self.session.commit()


