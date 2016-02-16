import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Zwinger(Base):
	"""ORM for Zwinger"""
	__tablename__ = 'zwinger'

	name = Column(String(80), nullable = False)
	address = Column(String(250))
	city = Column(String(80))
	state = Column(String(80))
	zipCode = Column(Integer(5))
	website = Column(String(250))
	id = Column(Integer, primary_key = True)

		

class Hund(Base):
	"""ORM for MenuItem"""
	__tablename__ = 'menu_item'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable = False)
	dateOfBirth = Column(Date)
	gender = Column(Enum('male','female', name='gender'), nullable = False)
	weight = Column(Numeric(10))
	picture = Column(String)
	zwinger_id = Column(Integer, ForeignKey('zwinger.id'))
	zwinger = relationship(Zwinger)
		


engine = create_engine('sqlite:///zwinger.db')
Base.metadata.create_all(engine)