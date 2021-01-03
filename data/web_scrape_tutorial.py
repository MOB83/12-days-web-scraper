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
first_movie_mscore = first_movie.find('span', class_='metascore favorable').text
# TODO - come back at number of votes section

print(f'{first_movie_title} released in {first_movie_year} with rating of {first_movie_rating} and metascore of {first_movie_mscore}')
