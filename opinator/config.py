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
SCRAPYD_URL = 'http://172.17.16.216:6800'
SCRAPY_PROJECT = 'scraper'

SECRET_KEY = 'ThIs7HardT0Gue$$'

SENTIMENT_SCORES = [
        ('Positive', 1),
        ('Negative', -1),
        ('Very Positive', 2),
        ('Very Negative', -2),
        ('Neutral', 0)
]

DEBUG = True
EMAIL_SEND = True
MAIL_ID = 'thelatelatif@gmail.com'
MAIL_PASS = 'alwayslate'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
DEBUG = True
MAIL_USE_SSL=False
MAIL_USERNAME = 'thelatelatif@gmail.com'
MAIL_PASSWORD = 'alwayslate'
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER= 'thelatelatif@gmail.com'
