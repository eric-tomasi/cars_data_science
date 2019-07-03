from scrape import run_scraper
from viz import clean_data, plot_trend


def main():
	'''main function which executes cars.com scraper, writes data to a csv, cleans it, and plots trend with a fitted curve'''

	run_scraper()

	plot_trend(clean_data())


main()