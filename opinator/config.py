import os

# The number of days for which the sentiment is valid
LIFESPAN = 60

#list of websites the project works
WEBSITES = ['amazon.in', 'flipkart.com', 'snapdeal.com']

# Mapping of website_name to spider name
WEBSITE_TO_SPIDER = {
                    'amazon.in': 'amazonin',
                    'flipkart.com': 'flipkartcom',
                    'snapdeal.com': 'snapdealcom'
}

#database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/opinator'

#scrapyd settings
SCRAPYD_URL = 'http://172.19.13.41:6800'
SCRAPY_PROJECT = 'scraper'

SECRET_KEY = 'ThIs7HardT0Gue$$'

SENTIMENT_SCORES = [
        ('Positive', 1),
        ('Negative', -1),
        ('Very Positive', 2),
        ('Very Negative', -2),
        ('Neutral', 0)
]

MAIL_ID = 'thelatelatif@gmail.com'
MAIL_PASS = 'alwayslate'
EMAIL_SEND = True
