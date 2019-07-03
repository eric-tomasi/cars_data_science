from ua import generate_random_ua
from bs4 import BeautifulSoup
import requests
import json
import csv
import numpy as np 
import time



def get_url():
	'''prompts user for url input and returns url as string'''

	url = input('provide valid cars.com url: ')

	#continually prompt users if url does not contain cars.com. 
	while 'cars.com' not in url:
		print('must be a cars.com search result url')

		url = input('provide valid cars.com url: ')

	return url



def generate_html(url):
	'''generates html as a string given the url to a website as input'''
 
	headers = {'user-agent': generate_random_ua()}

	source = requests.get(url, headers=headers).text

	return BeautifulSoup(source, 'lxml')



def run_scraper():
	'''scrapes cars.com url and writes data to a csv'''
	url = get_url()

	soup = generate_html(url)

	#gets the number of results displayed by query to known how many pages to loop through
	num_results = soup.find_all('script')[1].text 

	num_results = num_results[61:-2]

	num_results = json.loads(num_results)


	#gets list of urls by page so each one can be looped through
	urls = []	
	for page in range(num_results['page']['search']['totalNumPages']):
		new_url = url[:url.find('page=')+5] + str(page+1) + url[url.find('page=')+6:]
		urls.append(new_url)


	outfile = open('cars.com_scraper.csv', 'w')
	csv_writer = csv.writer(outfile, lineterminator = '\n')
	csv_writer.writerow(['listing_id', 'name', 'price', 'mileage', 'ext_color', 'int_color', 'transmission', 'drivetrain', 'make', 'model', 
		                    'condition', 'year', 'trim', 'bodystyle', 'dealer', 'state', 'rating', 'review_count', 'CPO', 'price2', 'mileage2'
		                    ])

	#loop through each url and write scraped results to a csv
	for url in urls:

		soup = generate_html(url)

		script = soup.find_all('script')[1].text 

		script = script[61:-2]

		script = json.loads(script)

		iteration = 0

		#name, price and mileage are all in main listing, but not always available so they are added to try/except blocks
		for listing in soup.find_all('div', class_='listing-row__details'):
		    name = listing.h2.text
		    name = name.strip()
		    
		    try:
		        price = listing.find('div', class_='payment-section')
		        price = price.find('span', class_='listing-row__price ').text
		        price = price.strip()
		    except:
		        price = None
		    
		    try:
		        mileage = listing.find('div', class_='payment-section')
		        mileage = mileage.find('span', class_='listing-row__mileage').text
		        mileage = mileage.strip()
		    except:
		        mileage = None
		    
		    
		    attribute = listing.find('ul', class_='listing-row__meta')
		    ext_color = attribute.find_all('li')[0].text
		    ext_color = ' '.join(ext_color.split())
		    int_color = attribute.find_all('li')[1].text
		    int_color = ' '.join(int_color.split())
		    trans = attribute.find_all('li')[2].text
		    trans = ' '.join(trans.split())
		    drivetrain = attribute.find_all('li')[3].text
		    drivetrain = ' '.join(drivetrain.split())

		    
		    # using the script section of the html contains additional dealer and vehicle info    
		    item = script['page']['vehicle'][iteration]
		    
		    iteration += 1
		    
		    csv_writer.writerow([item['listingId'], name, price, mileage, ext_color, int_color, trans, drivetrain, 
		                         item['make'], item['model'], item['stockType'], item['year'], item['trim'], item['bodyStyle'],
		                         item['seller']['name'], item['seller']['state'], item['seller']['rating'], item['seller']['reviewCount'],
		                         item['certified'], item['price'], item['mileage']
		                        ])


		#random time lag between loops ensures server is not overloaded with multiple requests per second
		lag = [10, 20, 35, 50, 30, 12, 45, 38, 60]
		lag = np.random.choice(lag)
		time.sleep(lag)
		    
		    
	outfile.close()