import os

BOT_NAME = 'scraper'

LOG_LEVEL = 'DEBUG'

SPIDER_MODULES = ['source.spiders']

ITEM_PIPELINES = {
'source.pipelines.scraperPipeline' : 300
}
