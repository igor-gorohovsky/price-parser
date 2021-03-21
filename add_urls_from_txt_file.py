from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from models.site_models import Urls
from models.db_config import config


def get_urls_from_txt():
    """Read urls to add them to the DB"""

    urls = []
    with open("urls.txt") as file:
        for line in file.readlines():
            urls.append(line)
    return urls


def get_list_for_query(urls):
    """ Create a list of instances of the Urls class.
    It need to add all urls to DB with one request. """

    instances = []
    for url in urls:
        instances.append(Urls(url=url))
    return instances


def main():
    engine = engine_from_config(config, prefix='db.')

    Session = sessionmaker(bind=engine)
    session = Session()

    urls = get_urls_from_txt()
    instances = get_list_for_query(urls)

    session.add_all(instances)
    session.commit()


if __name__ == '__main__':
    main()
