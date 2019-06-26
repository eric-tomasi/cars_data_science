from ua import generate_random_ua
from bs4 import BeautifulSoup
import requests
import json
import csv
import numpy as np 
import time


base_url = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=all&page=1&perPage=20&rd=99999&searchSource=SORT&sort=price-highest&zc=02038'

def generate_html(url):
	'''generates html as a string given the url to a website as input'''

	headers = {'user-agent': generate_random_ua()}

	source = requests.get(url, headers=headers).text

	return source



