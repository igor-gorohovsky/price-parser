from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.site_models import *


def main():
	engine = create_engine('postgresql+psycopg2:///parser')

	Session = sessionmaker(bind=engine)
	session = Session()

	urls = _get_urls_from_txt()
	instances = _create_list_of_instances_of_the_urls_class(urls)

	session.add_all(instances)
	session.commit()	


def _get_urls_from_txt():
	urls = []
	with open("urls.txt") as file:
		for line in file.readlines():
			urls.append(line)			
	return urls


def _create_list_of_instances_of_the_mapped_class(urls):
	instances = []
	for url in urls:
		instances.append(Urls(url=url))
	return instances

if __name__ == '__main__':
	main()