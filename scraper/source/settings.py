import os

BOT_NAME = 'scraper'

LOG_LEVEL = 'DEBUG'

SPIDER_MODULES = ['source.spiders']

ITEM_PIPELINES = {
'source.pipelines.scraperPipeline' : 300,
'source.pipelines.PostgresPipeline' : 400
}


#Postgres Settings
DB_HOST = 'localhost'
DB_NAME = 'opinator'
DB_USER = 'postgres'
DB_PASS = ''

#WSGI app location
WSGI_APP_IP = 'http://172.17.16.216:5001'
