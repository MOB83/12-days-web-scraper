from review_scrape import scrape_trustpilot_reviews
import pandas as pd

companies = [
    'wpengine.com',
    'kinsta.com',
    # 'www.a2hosting.com',
    # 'www.bluehost.com'
]

pages = [
    9,
    16,
    # 50,
    # 40
]

# Empty dataframe
reviews_df = None
for c, p in zip(companies, pages):
    url = f'https://ie.trustpilot.com/review/{c}?languages=all&page='
    data = scrape_trustpilot_reviews(c, url, p)
    if reviews_df is None:
        reviews_df = data
    else:
        reviews_df = pd.concat([reviews_df, data])

if reviews_df is not None:
    reviews_df.to_csv('./reviews_raw.csv', index=False)

# TODO: Load reviews for multiple competitors into a single dataset
# Kinsta, A2 Hosting, SiteGround, DreamHost, Bluehost, Hostwinds, InMotion Hosting,
# Cloudways, GoDaddy, WPX Hosting, Media Template Web Hosting, Pagely, Nexcess, Webflow, Liquid Web Managed Hosting
# Platform.sh, Lunarpress Internet Solutions, HostGator, Ionos 1&1 Hosting
