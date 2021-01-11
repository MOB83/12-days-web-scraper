from review_scrape import scrape_trustpilot_reviews

companies = [
    'wpengine.com',
    'kinsta.com',
    'www.a2hosting.com',
    'www.bluehost.com'
]

pages = [
    9,
    16,
    50,
    40
]

for c, p in zip(companies, pages):
    url = f'https://ie.trustpilot.com/review/{c}?languages=all&page='
    scrape_trustpilot_reviews(url, p)

# TODO: Load reviews for multiple competitors into a single dataset
# Kinsta, A2 Hosting, SiteGround, DreamHost, Bluehost, Hostwinds, InMotion Hosting,
# Cloudways, GoDaddy, WPX Hosting, Media Template Web Hosting, Pagely, Nexcess, Webflow, Liquid Web Managed Hosting
# Platform.sh, Lunarpress Internet Solutions, HostGator, Ionos 1&1 Hosting
