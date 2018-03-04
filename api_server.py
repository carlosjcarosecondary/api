#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask
import json, requests
app = Flask(__name__)

#GET REQUEST

@app.route('/readHello')
def getRequestHello():
	return "Hi, I got your GET Request!"

#POST REQUEST
@app.route('/createHello', methods = ['POST'])
def postRequestHello():
	return "I see you sent a POST message :-)"
#UPDATE REQUEST
@app.route('/updateHello', methods = ['PUT'])
def updateRequestHello():
	return "Sending Hello on an PUT request!"

#DELETE REQUEST
@app.route('/deleteHello', methods = ['DELETE'])
def deleteRequestHello():
	return "Deleting your hard drive.....haha just kidding! I received a DELETE request!"

@app.route('/foursquare', methods = ['GET'])
def foursquare():
	url = 'https://api.foursquare.com/v2/venues/explore'

	params = dict(
	  client_id='542SEDG5TXXHOPT1IITPXGMTT3AVPC3YEKIZKRO44ZXCQCRI',
	  client_secret='TTFJODOXG4YWM1AOGMJLURBHNUFVCAMDXTYJ4K1J2TAYYBRO',
	  v='20170801',
	  ll='40.7243,-74.0018',
	  query='coffee',
	  limit=1
	)

	resp = requests.get(url=url, params=params)
	data = json.loads(resp.text)
	print(data)
	return data

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	