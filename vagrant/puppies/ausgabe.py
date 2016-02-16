from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Zwinger, Hund
import datetime

engine = create_engine('sqlite:///zwinger.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def alleHunde():
	hunde = session.query(Hund)
	hunde = hunde.order_by(Hund.name)
	hunde = hunde.all()
	for hund in hunde:
		print hund.name


def zeigeWelpen():
	today = datetime.date.today()
	fromDate = today - datetime.timedelta(days = 182)
	hunde = session.query(Hund).filter(Hund.dateOfBirth >= fromDate)
	hunde = hunde.order_by(Hund.dateOfBirth.desc())
	hunde = hunde.all()
	for hund in hunde:
		print hund.name + ", " + str(hund.dateOfBirth)

def zeigeSchwereHunde():
	hunde = session.query(Hund)
	hunde = hunde.order_by(Hund.weight.desc())
	hunde = hunde.all()
	for hund in hunde:
		print hund.name + ", " + str(hund.weight)

def zeigeHundezwinger():
	hunde = session.query(Hund).order_by(Hund.zwinger_id)
	for hund in hunde:
		print hund.name.rjust(10, ' ') + ' : ' + hund.zwinger.name
