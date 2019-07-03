# Cars.com Web Scraper

The goal of this project is to scrape the search results of cars.com and record vehicle information such as price, mileage, year, trim, and others. There are plenty of solutions that exist today to determine the _current_ value of your car, but I have yet to find a solution that gives insight into a cars value in the _future_. Therefore, the aim is to gather datapoints on a particular car make/model and observe the selling price of that car for various mileages. Plotting the trend will help users to get an idea of how steep the depreciation curve really is for a car that they are planning to buy. As a fellow car enthusiast, taking into consideration the depreciation of a potential purchase is a huge factor in the decision to buy. 


## Getting Started
Follow these steps to run the car scraper yourself and compare the depreciation curves of any car of your choosing!

### Prerequisites 

To run the scraper, a few common packages from the scientific community are leveraged which can be installed using pip shown below:

```
pip install numpy
pip install pandas
pip install matplotlib
pip install seaboarn
pip install scipy
pip install beautifulsoup4
```

All other packages are already in the standard library. 

This scraper utilizes the requests library and beautifulsoup to scrape and parse through the HTML of the website. Numpy, pandas, and matplotlib are used for data cleaning and plotting of the trends. Scipy is used to fit a curve to the dataset. 

### Running Program

Simply execute main.py to run the program. You will be prompted to enter a valid cars.com url. Head over to cars.com and search for a single make/model. Please note that due to limitations in how cars.com is set up, this program will only be able to parse a maximum of 5,000 search results, so please apply filters to your query until you have under 5,000 records returned.

For best results, you should also filter for cars of a similar trim level as well. Once you have performed all desired filters on the cars.com website, simply copy and paste the url into the console when prompted by python. 

Scraping the web page can take several minutes, which is done intentionally, so that the cars.com server is not hit with multiple requests all at once. 

```
python main.py
provide valid cars.com url: https://www.cars.com/for-sale/searchresults.action/?dealerType=all&mdId=20884&mkId=20053&page=1&perPage=100&rd=500&searchSource=PAGINATION&sort=price-lowest&trId=32543&trId=23139&trId=29632&trId=23939&trId=57947&trId=57948&trId=53076&yrId=20199&yrId=20144&yrId=20200&yrId=20145&yrId=20201&yrId=27381&yrId=34923&yrId=39723&yrId=47272&yrId=51683&yrId=56007&yrId=58487&yrId=30031936&yrId=35797618&yrId=36362520&zc=02038
```

### Outputs

There are two main outputs:

```
cleaned_data.csv
trend.png
```

The cleaned_data.csv file is a log of all of the search results returned by your query on cars.com. So, if you are looking for BMW 3-series results, and filtered for the 335/340i trims, all of those results will be parsed and cleaned in this csv file. Data cleaning involved using multiple paramters in the html to determine price and mileage, as well as formatting datatypes and stripping unecedssary text that would inhibit a user's ability to performa analytics. 

The trend.png is a visual of all of the data points that were scraped. The x-axis is mileage while the y-axis is price. A line of best fit is shown in red as well. This trend can show you an expectation of how the car may depreciate in the future as more miles are put on the vehicle. 


## Caveats

The goal is to get a general sense of the steepness of the depreciation curve for any car that is given. Scipy's curve_fit function is used to apply a line of best fit based on a least squares estimation. It should not, however, be confused for a production ready predictive model. Each car behaves differently in that some depreciation curves are so steep in the beginning of its life, that the trend almost appears more logarithmic. However, for this program, an exponential decay function was used, which seems to be the most appropriate for a large number of cars. 

On the contrary, some cars seem to have very little correlation with price and mileage and thus, no equation is really a best fit. Further more, there are outliers in the car world (classics, high end vehicles like ferrari, and rare/collectible cars) that can actually _appreciate_ in value. Clearly an exponential decay function is not useful for these cars. 

The decision was made to leave in the fitted curve as it can represent a general direction of the trend and can show users the steepness of the curve more easily, despite its known shortcomings. 

The data and trend added to this repo is for a BMW 335/340i for reference

### Ackowledgements 
All work was completed by Eric Tomasi. etomasi2323@gmail.com
