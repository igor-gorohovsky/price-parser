from sqlalchemy import *
from sqlalchemy.orm import declarative_base

engine = create_engine('postgresql+psycopg2:///parser', echo=True)


Base = declarative_base()


class Urls(Base):
	__tablename__ = 'urls'

	id = Column(Integer, primary_key=True)
	url = Column(String, nullable=False, unique=True)


class Prices(Base):
	__tablename__ = 'prices'
	__table_args__ = (PrimaryKeyConstraint('url_id', 'date'), {})

	url_id = Column(Integer, ForeignKey('urls.id'))
	date = Column(DateTime, nullable=False)
	price = Column(String(10))


if __name__ == '__main__':
	Base.metadata.create_all(engine)