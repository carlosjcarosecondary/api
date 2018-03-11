from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = '542SEDG5TXXHOPT1IITPXGMTT3AVPC3YEKIZKRO44ZXCQCRI'
foursquare_client_secret = 'TTFJODOXG4YWM1AOGMJLURBHNUFVCAMDXTYJ4K1J2TAYYBRO'
google_api_key = 'AIzaSyBpIJWMQp41bF_QyxBTLzcx5vCAeCDSPT4'

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  if request.method == 'GET':
  	restaurants = session.query(Restaurant).all()
  	return jsonify(restaurants = [i.serialize for i in restaurants])

  elif request.method == 'POST':
  	#location = request.args.get('location')
  	#mealtype = request.args.get('mealType')
    location = 'Lima+Peru'
    mealtype = 'sushi'
    restaurant_info = findARestaurant(mealtype, location)
    if restaurant_info != 'No Restaurants Found':
  		restaurant = Restaurant(restaurant_name = restaurant_info['name'],
  								restaurant_address = restaurant_info['address'],
  								restaurant_image = restaurant_info['image'])

  		session.add(restaurant)
  		session.commit()
  		return jsonify(restaurant = restaurant.serialize)
    else:
  		return jsonify({"error":"No restaurants found for %s and %s"%(location, mealtype)})

    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  restaurant = session.query(Restaurant).filter_by(id = id ).one()
  if request.method == 'GET':
  	return jsonify(restaurant = restaurant.serialize)
  # UPDATE
  elif request.method == 'PUT':
  	address = request.args.get('address')
  	name = request.args.get('name')
  	image = request.args.get('get')

  	if name:
  		restaurant.restaurant_name = name
  	if address:
  		restaurant.restaurant_address = address
  	if image:
  		restaurant.restaurant_image = image
  	session.commit()
  	return jsonify(restaurant = restaurant.serialize)
  # DELETE
  elif request.method == 'DELETE':
  	session.delete(restaurant)
  	session.commit()
  	return jsonify({'message':'Restaurant has been deleted'})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)