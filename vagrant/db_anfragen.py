# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getAllRestaurants():
	restaurants = session.query(Restaurant)
	restaurants = restaurants.order_by(Restaurant.name)
	return restaurants.all()

def create_restaurant(name):
	session.add(Restaurant(name = name))
	session.commit()

def getRestaurant(id):
	restaurants = session.query(Restaurant).filter(Restaurant.id == id)
	return restaurants.one()

def updateRestaurant(new_name, id):
	restaurant = getRestaurant(id)
	restaurant.name = new_name
	session.commit()

def deleteRestaurant(id):
	restaurant = getRestaurant(id)
	session.delete(restaurant)
	session.commit()
