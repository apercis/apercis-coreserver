import smtplib
import models
import random
import string
import bcrypt

import hashlib
import opinator

from functools import wraps

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    """ Generates a random identifier for the given size and using the
    specified characters.
    If no size is specified, it uses 15 as default.
    If no characters are specified, it uses ascii char upper case and
    digits.
    :arg size: the size of the identifier to return.
    :arg chars: the list of characters that can be used in the
        idenfitier.
    """
    return ''.join(random.choice(chars) for x in range(size))


def send_email(text, subject, to_mail,
               mail_id=None, in_reply_to=None,
               project_name=None):  # pragma: no cover
    ''' Send an email with the specified information.
    :arg text: the content of the email to send
    :arg subject: the subject of the email
    :arg to_mail: a string representing a list of recipient separated by a
        coma
    :kwarg mail_id: if defined, the header `mail-id` is set with this value
    :kwarg in_reply_to: if defined, the header `In-Reply-To` is set with
        this value
    '''
    if not to_mail:
        return

    if not opinator.APP.config.get('EMAIL_SEND', True):
        print '******EMAIL******'
        print 'To: %s' % to_mail
        print 'Subject: %s' % subject
        print 'in_reply_to: %s' % in_reply_to
        print 'mail_id: %s' % mail_id
        print 'Contents:'
        print text.encode('utf-8')
        print '*****/EMAIL******'
        return

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(mail_id, APP.config['MAIL_PASS'])

        msg = "\r\n".join([
            "From: %s" % mail_id,
            "To: %s" % to_mail,
            "Subject: %s" % subject,
            "",
            "%s" % text
            ])

        smtpserver.sendmail(mail_id, to_mail, msg)
        smtpserver.close()
        print 'successfully sent mail'
    except:
        print 'failed to send mail'


def search_product(session, token=None, url=None, product_id=None):
    query = session.query(
        models.Product
    ).order_by(
        models.Product.product_id
    )

    if product_id is not None:
        query = query.filter(
                models.Product.product_id == product_id
        )

    if token is not None:
        query = query.filter(
            models.Product.token == token
        )

    if url is not None:
        query = query.filter(
            models.Product.url == url
        )

    output = None
    if any([product_id, token, url]):
        output = query.first()

    return output


def search_reviews(session, token=None):
    '''Search the db to get all the reviews '''
    query = session.query(
            models.Review
    ).order_by(
            models.Review.id
    )

    if token is not None:
        query = query.filter(
                models.Review.product_token == token
        )

    output = None
    if token:
        output = query.all()

    return output


def search_positive_reviews(session, token=None):
    '''Search the db to get all the reviews '''
    query = session.query(
            models.Review
    ).order_by(
            models.Review.id
    )

    if token is not None:
        query = query.filter(
                models.Review.product_token == token
        )
        query = query.filter(
                models.Review.sentiment_id == 1
        )
        query = query.filter(
                models.Review.sentiment_id == 3
        )

    output = None
    if token:
        output = query.all()

    return output


def search_negative_reviews(session, token=None):
    '''Search the db to get all the reviews '''
    query = session.query(
            models.Review
    ).order_by(
            models.Review.id
    )

    if token is not None:
        query = query.filter(
                models.Review.product_token == token
        )
        query = query.filter(
                models.Review.sentiment_id == 2
        )
        query = query.filter(
                models.Review.sentiment_id == 4
        )

    output = None
    if token:
        output = query.all()

    return output


def search_sentiment(session, sentiment=None, id=None):
    ''' Search the db to get the sentiment/scores '''
    query = session.query(
            models.Sentiment
    ).order_by(
            models.Sentiment.id
    )

    if sentiment is not None:
        query = query.filter(
                models.Sentiment.sentiment == sentiment
        )

    if id is not None:
        query = query.filter(
                models.Sentiment.id == id
        )

    output = None
    if any([id, sentiment]):
        output = query.first()

    return output


def search_website(session, website=None, id=None):
    ''' Return the website object from the db '''
    query = session.query(
            models.Website
    ).order_by(
            models.Website.id
    )

    if website is not None:
        query = query.filter(
                models.Website.website == website
        )

    if id is not None:
        query = query.filter(
                models.Website.id == id
        )

    output = None
    if any([id, website]):
        output = query.first()

    return output
