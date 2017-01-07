import requests
import json

class APICall:

	def __init__(self, access_token):
		self.author = 'MD ISLAM'
		self.access_token = access_token

	def makeRequest(self, url):
		return requests.get(url+'&access_token='+self.access_token).text

	def makeRequestPost(data, url):
		return requests.get(url+'&access_token='+self.access_token, data).text