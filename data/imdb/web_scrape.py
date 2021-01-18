# Script to perform web scraping of IMDB
# From this reousrce - https://www.dataquest.io/blog/web-scraping-beautifulsoup/
import os
from time import time, sleep
from random import randint
from warnings import warn

from requests import get
from bs4 import BeautifulSoup
import pandas as pd

# Define properties we want to scrape
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Setup monitoring variables
start_time = time()
requests = 0
request_limit = 72

# Configure url parameters
pages = [str(i) for i in range(1, 5)]
years_url = [str(i) for i in range(2000, 2018)]

for year_url in years_url:
    for page in pages:

        # Request the page
        url = f'http://www.imdb.com/search/title?release_date={year_url}&sort=num_votes,desc&page={page}'
        response = get(url)

        # Pause the loop to limit access to the server
        sleep(randint(8, 15))

        # Monitor the request
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        os.system('clear')

        if response.status_code != 200:
            warn(f'Request: {requests}l; Status Code: {response}')

        if requests > request_limit:
            warn('Number of requests have exceeded expectation')
            break

        page_html = BeautifulSoup(response.text, 'html.parser')
        mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

        for container in mv_containers:
            if container.find('div', class_='ratings-metascore') is not None:
                names.append(container.h3.a.text)
                years.append(container.find('span', class_='lister-item-year text-muted unbold').text)
                imdb_ratings.append(float(container.strong.text))
                metascores.append(int(container.find('span', class_='metascore').text))
                votes.append(int(container.find('span', attrs={'name': 'nv'})['data-value']))

# Merge scraped data into a dataframe
mv_rating_df = pd.DataFrame(
    {
        'movie': names,
        'year': years,
        'imdb': imdb_ratings,
        'metascore': metascores,
        'votes': votes
    }
)

# Save the dataframe
mv_rating_df.to_csv('./imdb_movies.csv', index=False)