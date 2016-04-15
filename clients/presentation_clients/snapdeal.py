import os
os.chdir('/home/vivek/opinator/opinator/scraper')
os.system("scrapy crawl snapdealcom -a url=%s" % 'http://www.snapdeal.com/product/intex-cloud-breeze-8gb-grey/671476050074#bcrumbLabelId:175')
