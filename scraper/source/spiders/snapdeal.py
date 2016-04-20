import requests
import datetime
import scrapy.item
import scrapy.selector
import scrapy.linkextractors
import scrapy.spiders
import scrapy.conf
import scrapy.crawler
from scrapy.http.request import Request

import source
import source.items
import source.settings

class Snapdeal(scrapy.spiders.CrawlSpider):
    """Extracts reviews from snapdeal.com"""

    name = 'snapdealcom'
    allowed_domains = ['www.snapdeal.com']
    start_url_frame = 'http://snapdeal.com/product/'

    def __init__(self, url, token, **kwargs):
        self.url = self.clean_url(url)
        self.token = token
        self.start_urls = [self.url]

        pagination_regex_list = [r'http://www.snapdeal.com/product/.*']
        self.paginate = scrapy.linkextractors.LinkExtractor(
                allow = pagination_regex_list,
                restrict_xpaths = (
                    '//*[@class="pagination"]//a/i[@class="sd-icon sd-icon-next "]/parent::node()'
                )
        )

        self.rules = [
            scrapy.spiders.Rule(
                self.paginate, callback='parse_items', follow=True
            ),
        ]

        super(Snapdeal, self).__init__(url, **kwargs)


    def clean_url(self, url):
        ''' Clean the url: remove the words after # and add /reviews '''
        url_ = url[:url.find('#')]
        url_ = "".join(url_)
        url_ += '/reviews'
        return url_

    def parse_start_url(self, response):
        return self.parse_items(response)


    def parse_items(self, response):
        hxs = scrapy.Selector(response)
        item = source.items.scraperItem()
        item['reviews'] = self.get_reviews(hxs)
        item['is_verified'] = self.is_verified(hxs)
        item['date'] = self.get_date(hxs)
        item['token'] = self.token
        next_url = self.__get_next_url(hxs)
        if next_url != '':
            yield Request(next_url, callback=self.parse_items)
        yield item

    def __get_next_url(self, hxs):
        url_path = hxs.xpath('//*[@class="pagination"]//a/i[@class="sd-icon sd-icon-next "]/parent::node()/@href')
        try:
            url = url_path.extract()[0].strip()
            return url
        except:
            return ''

    def get_date(self, hxs):
        date_path = hxs.xpath('//div[@class="date LTgray"]/text()')
        try:
            return date_path.extract()[0].strip()
        except IndexError:
            return ''


    def get_reviews(self, hxs):
        reviews_path = hxs.xpath('//div[contains(@id, "_reviewDiv")]//p')
        try:
            revs = reviews_path.extract()
            review = ''
            for i in revs:
                review += i.strip()
            return review
        except IndexError:
            return ''


    def is_verified(self, hxs):
        verify_path = hxs.xpath('//div[@class="LTgray light-font"]/text()')
        try:
            temp = verify_path.extract()[0].strip()
            return True
        except IndexError:
            return False


    def get_stars_count(self, hxs):
        stars_count_path = hxs.xpath(' ')
        try:
            return stars_count.extract[0].strip()
        except IndexError:
            return ''


    def closed(self, reason):
        ''' Method called when the scraper is closed '''

        a = requests.post('http://172.19.13.41:5000/process_reviews', data={'token': self.token})
        return
