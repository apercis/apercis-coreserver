import os
os.chdir('/home/vivek/opinator/opinator/scraper')
os.system('scrapy crawl amazonin -a product_id=%s' % '1408856778')
