# From this reousrce - https://www.dataquest.io/blog/web-scraping-beautifulsoup/
from requests import get
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')

movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

first_movie = movie_containers[0]
first_movie_title = first_movie.h3.a.text
first_movie_year = first_movie.find('span', class_='lister-item-year text-muted unbold').text
first_movie_rating = float(first_movie.strong.text)
first_movie_mscore = int(first_movie.find('span', class_='metascore favorable').text)
first_movie_votes = int(first_movie.find('span', attrs={'name': 'nv'})['data-value'])

print(
    f'{first_movie_title} released in '
    f'{first_movie_year} with rating of '
    f'{first_movie_rating} and metascore of '
    f'{first_movie_mscore} with '
    f'{first_movie_votes} votes')


# Actual scraping
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

for container in movie_containers:
    if container.find('div', class_='ratings-metascore') is not None:
        names.append(container.h3.a.text)
        years.append(container.find('span', class_='lister-item-year text-muted unbold').text)
        imdb_ratings.append(float(container.strong.text))
        metascores.append(int(container.find('span', class_='metascore').text))
        votes.append(int(container.find('span', attrs={'name': 'nv'})['data-value']))

import pandas as pd
test_df = pd.DataFrame(
    {
        'movie': names,
        'year': years,
        'imdb': imdb_ratings,
        'metascore': metascores,
        'votes': votes
    }
)

print(test_df.info())
print(test_df)

# TODO - start off from Script for Multiple Pages
