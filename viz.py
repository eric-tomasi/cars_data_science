import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def clean_data():
	'''cleans scraped csv file by manipulating columns to be used for visualization'''

	df = pd.read_csv('bmw_3series.csv')


	#clean price column. Utilize price column (shown to end user) unless null, then show price2
	df['price'] = df['price'].replace({'\$': '', ',': '', 'MSRP': ''}, regex=True)

	df['price'] = np.where(df['price'] =='Not Priced', None, df['price'])

	df['price'] = df['price'].astype(float)

	df['price'] = np.where(df['price'].isnull(), df['price2'], df['price'])


	#clean mileage column. Utilize mileage column (shown to end user) unless null, then show mileage2

	df['match'] = np.where(df['price'] == df['price2'], 1,0)

	print(df[['price', 'price2', 'match']])


clean_data()