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

	return df


def fit_curve():
	'''Fits an exponential decay curve to the dataset. returns dataframe with the curve points for plotting'''
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




'''
df = clean_data()

xdata = np.array([10, 2513,4580,11323,25425,25425,
31235,
35570,
52349,
61142,
82344,
113276,
122388,
154321
])
ydata = np.array([67660,
63285,
52235,
41950,
34500,
34900,
33440,
32600,
26995,
23999,
19255,
15995,
14299,
12450
])

#define exponential decay func
def exponential_decay(x,a,t, y0):
	return a * np.exp(-x * t) + y0

#find optimal paramaters and covariance
popt, pcov = curve_fit(exponential_decay, xdata, ydata)

x_fit = np.linspace(np.min(xdata), np.max(xdata), 10000)
y_fit = exponential_decay(x_fit, *popt)
print(popt)

plt.plot(xdata, ydata, 'r', label='data')
plt.plot(x_fit, y_fit, 'b', label='fit')

plt.show()'''

plot_trend(clean_data())
