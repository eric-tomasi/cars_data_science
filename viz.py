import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def clean_data():
	'''returns a cleaned csv file by manipulating columns in original scraped csv to be used for visualization'''

	df = pd.read_csv('bmw_3series.csv')


	#clean price column. Utilize price column (shown to end user) unless null, then show price2
	df['price'] = df['price'].replace({'\$': '', ',': '', 'MSRP': ''}, regex=True)

	df['price'] = np.where(df['price'] =='Not Priced', None, df['price'])

	df['price'] = df['price'].astype(float)

	df['price'] = np.where(df['price'].isnull(), df['price2'], df['price'])


	#clean mileage column. Utilize mileage column (shown to end user) unless null, then show mileage2
	df['mileage'] = df['mileage'].replace({'mi.': '', ',': '', ' ': '', '--': ''}, regex=True)
	df['mileage'] = df['mileage'].replace({'': None})
	
	df['mileage'] = df['mileage'].astype(float)

	df['mileage'] = np.where(df['mileage'].isnull(), df['mileage2'], df['mileage'])


	#clean ext_color, int_color, transmission, and drivetrain columns to strip out labels
	df['ext_color'] = df['ext_color'].str.replace('Ext. Color: ', '')
	df['int_color'] = df['int_color'].str.replace('Int. Color: ', '')
	df['transmission'] = df['transmission'].str.replace('Transmission: ', '')
	df['drivetrain'] = df['drivetrain'].str.replace('Drivetrain: ', '')

	#remove columns that are no longer needed
	df.drop(['price2', 'mileage2'], 1, inplace=True)

	return df
