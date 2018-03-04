from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "542SEDG5TXXHOPT1IITPXGMTT3AVPC3YEKIZKRO44ZXCQCRI"
foursquare_client_secret = "TTFJODOXG4YWM1AOGMJLURBHNUFVCAMDXTYJ4K1J2TAYYBRO"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?
	#client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s'%(foursquare_client_id,foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(content)
	#3. Grab the first restaurant
	venue_id = result['response']['venues'][0]['id']
	venue_name = result['response']['venues'][0]['name']
	venue_address = result['response']['venues'][0]['location']
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815'%(venue_id,foursquare_client_id,foursquare_client_secret))
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(content)
	#5. Grab the first image
	if result['response']['photos']['items']:
		image_url = result['response']['photos']['items'][0]['source']['url']
	else:
		image_url = 'ALIANZA LIMA'

	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url	
	outcome = {'name':venue_name, 'address':venue_address, 'image':image_url}
	return outcome

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")