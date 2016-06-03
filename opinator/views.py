import os
import json
import flask
import requests
#import pandas as pd
from datetime import datetime, timedelta

import opinator
from opinator import APP, forms, SESSION
from opinator.lib import models
from opinator.lib.nlp import get_sentiment_of_review
from analyzer.summary.summary_tool import BushyPath
from analyzer.summary.sums  import SummaryUsingGooglePageRank


@APP.route('/home', methods=['POST'])
def index():
    ''' View for the initial request from the plugin '''

    form = forms.RequestForm(csrf_enabled=False)
    if form.validate_on_submit():
        product_id = form.product_id.data
        url = form.url.data
        website = form.website.data
        email = form.email.data

        try:
            spiders = APP.config.get('WEBSITE_TO_SPIDER', None)
            spider = spiders[website]
        except:
            return flask.json.jsonify({'status': False})

        #get the website
        website_ = opinator.lib.search_website(SESSION, website=website)
        website_id = website_.id

        #check if already processed
        try:
            if website_id == 1:
                product_ = opinator.lib.search_product(SESSION, product_id=product_id)
                if product_:
                    sentiment = product_.sentiment_id
                    bushy_positive_summary = product_.bushy_positive_summary
                    bushy_negative_summary = product_.bushy_negative_summary
                    gr_positive_summary = product_.gr_positive_summary
                    gr_negative_summary = product_.gr_negative_summary
                    jsonout = {\
                            'summary': {
                                'bushy': {\
                                    'negative': bushy_negative_summary,
                                    'positive': bushy_positive_summary,
                                },
                                'google_page_rank': {\
                                    'negative': gr_negative_summary,
                                    'positive': gr_positive_summary,
                                }
                            }
                    }
                    return flask.json.jsonify(jsonout)
            elif website_id == 2 or website_id == 3:
                product_ = opinator.lib.search_product(SESSION, url=url)
                if product_:
                    sentiment = product_.sentiment_id
                    bushy_positive_summary = product_.bushy_positive_summary
                    bushy_negative_summary = product_.bushy_negative_summary
                    gr_positive_summary = product_.gr_positive_summary
                    gr_negative_summary = product_.gr_negative_summary
                    jsonout = {\
                            'summary': {
                                'bushy': {\
                                    'negative': bushy_negative_summary,
                                    'positive': bushy_positive_summary,
                                },
                                'google_page_rank': {\
                                    'negative': gr_negative_summary,
                                    'positive': gr_positive_summary,
                                }
                            }
                    }
                    return flask.json.jsonify(jsonout)
        except:
            print 'wrong initialy'
            return 'something sucks'

        #generate token for identifying reviews for further processings
        token = opinator.lib.id_generator()

        payload = {
                'product_id': product_id,
                'url': url,
                'spider': spider,
                'project': APP.config.get('SCRAPY_PROJECT', 'scraper'),
                'token': token,
        }

        scrapyd_url = APP.config.get('SCRAPYD_URL', 'http://localhost:6800')
        scrapyd_schedule_url = scrapyd_url + '/schedule.json'

        job = requests.post(scrapyd_schedule_url, data=payload)
        job = job.json()

        try:
            if job['status'] == 'ok':
                product = models.Product(
                                    product_id=product_id,
                                    url=url,
                                    website_id=website_id,
                                    email=email,
                                    token=token)
                SESSION.add(product)
                SESSION.commit()
            else:
                return flask.json.jsonify({'status': False})
        except:
            print 'SQLALCHEMY error!!!'
            SESSION.rollback()
            return flask.json.jsonify({'status': False})
        return flask.json.jsonify({'status': True})
    return flask.json.jsonify({'status': False})


@APP.route('/process_reviews', methods=['POST'])
def process_reviews():
    ''' check '''

    if not flask.request.form.get('token', None):
        return 'Something still sucks'

    token = flask.request.form.get('token')

    try:
        reviews = opinator.lib.search_reviews(SESSION, token=token)
        if not reviews:
            return 'Something till sucks'
    except:
        print 'Some error in querying reviews'
        return 'something still sucks'

    for review in reviews:
        sentiment_ = get_sentiment_of_review(review.review)
        try:
            sentiment_obj = opinator.lib.search_sentiment(SESSION, sentiment=sentiment_)
        except:
            print 'can not find sentiment in db'
            return 'sentiment not found in db, time to die'
        sentiment = sentiment_obj.id
        try:
            review.sentiment_id = sentiment
            SESSION.add(review)
            SESSION.commit()
        except:
            SESSION.rollback()
            print 'can not update sentiment of a review'
            return 'something still sucks'

    #try:
    #positive_reviews = opinator.lib.search_positive_reviews(SESSION, token=token)
    #negative_reviews = opinator.lib.search_negative_reviews(SESSION, token=token)
    reviews = opinator.lib.search_reviews(SESSION, token=token)

    positive_reviews = []
    negative_reviews = []
    for r in reviews:
        if r.sentiment_id == 1 or r.sentiment_id == 3:
            positive_reviews.append(r)
        elif r.sentiment_id == 2 or r.sentiment_id == 4:
            negative_reviews.append(r)

    #except:
        #print 'can not query positive and negative reviews'
        #return 'something in sqlalchemy querying still sucks'

    pos_revs_string = ''
    for r in positive_reviews:
        pos_revs_string += ' '
        pos_revs_string += str(r.review)

    neg_revs_string = ''
    for r in negative_reviews:
        neg_revs_string += ' '
        neg_revs_string += str(r.review)


    try:
        bushy_pos_obj = BushyPath(pos_revs_string)
        bushy_positive_summary = bushy_pos_obj.summarize()

        bushy_neg_obj = BushyPath(neg_revs_string)
        bushy_negative_summary = bushy_neg_obj.summarize()
    except:
        print 'Error finding summary using bushy path'
        bushy_positive_summary = None
        bushy_negative_summary = None


    product = opinator.lib.search_product(SESSION, token=token)
    product.bushy_positive_summary = bushy_positive_summary
    product.bushy_negative_summary = bushy_negative_summary

    try:
        SESSION.add(product)
        SESSION.commit()
    except:
        SESSION.rollback()
        print 'Bushy path could not be updated'

    try:
        gr_pos_obj = SummaryUsingGooglePageRank(pos_revs_string)
        gr_positive_summary = gr_pos_obj.summarize()

        gr_neg_obj = SummaryUsingGooglePageRank(neg_revs_string)
        gr_negative_summary = gr_neg_obj.summarize()
    except:
        print 'Error while finding summary using google page rank'
        gr_positive_summary = None
        gr_negative_summary = None


    product.gr_positive_summary = gr_positive_summary
    product.gr_negative_summary = gr_negative_summary

    try:
        SESSION.add(product)
        SESSION.commit()
    except:
        SESSION.rollback()
        print 'Google page rank could not be updated to db'

    print 'Vivek, You are a champion'
    send_summary_email(product)
    return 'suck it'


def send_summary_email(product):
    ''' Send the summary via email '''
    text = """ Dear %s,
    Thanks for using Opinator.
    Here is the summary of the reviews:
    1. Bushy Path - Positive:

        %s

    2. Bushy Path - Negative:

        %s

    3. Google Page Rank Algo - Positive:

        %s

    4. Google Page Rank Algo - Negative:

        %s


    Once again, Thanks for using Opinator.
    """ % (product.email, product.bushy_positive_summary,
            product.bushy_negative_summary, product.gr_positive_summary,
            product.gr_negative_summary)

    subject = """[Opinator] Summary of the product reviews"""
    to_mail = str(product.email)
    mail_id = APP.config['MAIL_ID']

    print 'about to call email'
    #opinator.lib.send_email(text, subject, to_mail, mail_id)
    return
