import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit


def clean_data():
	'''returns a cleaned csv file by manipulating columns in original scraped csv to be used for visualization'''

	df = pd.read_csv('cars.com_scraper.csv')

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
	df.dropna(subset=['price', 'mileage'], inplace=True)

	df.to_csv('cleaned_data.csv')

	return df


def fit_curve():
	'''Fits an exponential decay curve to the dataset. returns fitted x and y values for plotting'''
	df = clean_data()

	# get x and y
	x_data = df['mileage'].values
	y_data = df['price'].values

	def exponential_decay(x,a,r):
		return a*(1-r)**x

	#find optimal paramaters and covariance
	popt, pcov = curve_fit(exponential_decay, x_data, y_data)

	x_fit = np.linspace(np.min(x_data), np.max(x_data), 10000)
	y_fit  = exponential_decay(x_fit, *popt)

	return x_fit, y_fit



def plot_trend(df):

	#set up figure and alter settings
    fig, ax1 = plt.subplots(figsize=(20,8.5))
    plt.rcParams.update({'font.size':14})
    sns.set()

    #plot scatter of price by mileage
    ax1.scatter(df['mileage'], df['price'], color='xkcd:cobalt', label='Price Data', linewidth=1.0)
    ax1.set_xlabel('Mileage')
    ax1.set_ylabel('Price')
    ax1.set_xticks(np.arange(0, df['mileage'].max(), 12000))

    #plot trendline
    x_fit, y_fit = fit_curve()

    ax1.plot(x_fit, y_fit, 'r', linewidth=3.5, label='Fitted Curve')

    #set title, legend, and savefig
    plt.title('Price by mileage')
    plt.legend(loc='upper right')
    fig.savefig('trend.png', dpi=fig.dpi)
