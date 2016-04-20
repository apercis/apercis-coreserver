import psycopg2
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASS
from scrapy.exceptions import DropItem

class scraperPipeline(object):
    def process_item (self, item, spider):
        if item['is_verified'] == False:
            raise DropItem('Not a verified review')

        if item['reviews'].strip() == '':
            raise DropItem('Empty review')

        item['reviews'] = item['reviews'].replace("'", "\"")
        return item


class PostgresPipeline(object):
    ''' Pipeline the items to postgres db '''

    def __init__(self):
        ''' Initiate the db connections '''
        self.connection_str = "host=%s dbname=%s user=%s password=%s" % ( \
                                DB_HOST, DB_NAME, DB_USER, DB_PASS)
        self.connection = psycopg2.connect(self.connection_str)
        self.cursor = self.connection.cursor()


    def process_item(self, item, spider):
        ''' Actual pipelining to the db '''
        #try:
        self.cursor.execute("""INSERT INTO reviews (product_token, date, \
                is_verified, review) values ('%s', '%s', '%s','%s')""" % ( \
                str(item['token']), str(item['date']), str(item['is_verified']), str(item['reviews'])))
        self.connection.commit()
        #except:
            #print 'Error while pipelining data'
            #pass
        return item
