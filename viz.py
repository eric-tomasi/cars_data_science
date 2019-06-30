import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def clean_data():
	'''returns a cleaned csv file by manipulating columns in original scraped csv to be used for visualization'''

	df = pd.read_csv('bmw_3series.csv')
	df = df[df['model'].isin(['335', '340'])]


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


def plot_trend(df):

	#set up figure and alter settings
    fig, ax1 = plt.subplots(figsize=(20,8.5))
    plt.rcParams.update({'font.size':14})
    sns.set()

    #plot scatter of price by mileage
    ax1.scatter(df['mileage'], df['price'], color='xkcd:cobalt', label='Price', linewidth=1.0)
    ax1.set_xlabel('Mileage')
    ax1.set_ylabel('Price')
    ax1.set_xticks(np.arange(0, df['mileage'].max(), 12000))

    #set title, legend, and savefig
    plt.title('Price by mileage')
    plt.legend(loc='upper right')
    fig.savefig('trend.png', dpi=fig.dpi)


plot_trend(clean_data())