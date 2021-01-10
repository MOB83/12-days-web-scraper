# Based off this tutorial
# https://towardsdatascience.com/customer-reviews-identify-your-strengths-and-weaknesses-with-the-help-of-web-scraping-data-b87a3636ef55

# Scrape from - 'https://www.trustpilot.com/review/flixbus.com?languages=all&page='
import datetime
import os
import pandas as pd
from random import randint
from time import sleep, time
from warnings import warn

from requests import get
from bs4 import BeautifulSoup


def scrape_trustpilot_reviews(PATH, n_pages):
    """
    Method to scrape data from trust pilot reviews
    :param PATH: The path to scrape review data from
    :param n_pages: The number of pages to scrape
    :param sleep_time: The time to sleep between requests to avoid overloading the server
    :return: Dataframe containing the review data
    """

    # Review properties
    names = []
    ratings = []
    headers = []
    reviews = []
    dates = []
    locations = []

    # Setup monitoring variables
    start_time = time()
    requests = 0
    request_limit = 72

    # For each page specified, get reviews
    for p in range(n_pages):

        url = f'{PATH}{p}'
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

        # Identify page areas of interest
        page_html = BeautifulSoup(requests.text, 'html.parser')
        review_containers = page_html.find_all('div', class_='review-info__body')
        user_containers = page_html.find_all('div', class_='customer-info__details')
        rating_containers = page_html.find_all('div', class_='review-info__header__verified')
        date_container = page_html.find_all('div', class_='header__verified__date')
        profile_container = page_html.find_all('div', class_='review__consumer-information')

        for x in range(len(date_container)):
            review_c = review_containers[x]
            headers.append(review_c.h2.a.text)
            reviews.append(review_c.p.text)

            reviewer = user_containers[x]
            names.append(reviewer.h3.text)

            rating = rating_containers[x]
            ratings.append(rating.div.attrs['class'][1][12])

            date = date_container[x]
            dates.append(datetime.datetime.strptime(date.time.attrs['datetime'][0:10], '%Y-%m-%d').date())

            prof = profile_container[x]
            link = 'https://www.trustpilot.com' + prof.a['href']
            c_profile = get(f'{link}')
            profile_html = BeautifulSoup(c_profile.text, 'html.parser')
            cust_container = profile_html.find('div', class_='user-summary-location')
            locations.append(cust_container.text)

    reviews_df = pd.DataFrame(
        {
            'Header': headers,
            'Review': reviews,
            'Rating': ratings,
            'Name': names,
            'Location': locations,
            'Date': dates
        }
    )

    reviews_df.to_csv('./reviews_raw.csv', index=False)