__requires__ = ['SQLAlchemy >= 0.8', 'jinja2 >= 2.4']

import datetime
import logging
import json

import flask
import sqlalchemy as sa


from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship

BASE = declarative_base()

import opinator
from opinator import APP

def create_tables(db_url, alembic_ini=None, debug=False):
    """ Create the tables in the database using the information from the
    url obtained.
    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.
    """

    engine = create_engine(db_url, echo=debug)
    BASE.metadata.create_all(engine)
    if db_url.startswith('sqlite:'):
        def _fk_pragma_on_connect(dbapi_con, con_record):
            ''' Tries to enforce referential constraints on sqlite. '''
            dbapi_con.execute('pragma foreign_keys=ON')
        sa.event.listen(engine, 'connect', _fk_pragma_on_connect)

    if alembic_ini is not None:
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:

        # Ignore the warning missing alembic
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    scopedsession = scoped_session(sessionmaker(bind=engine))
    BASE.metadata.bind = scopedsession
    #create default values in a few tables
    create_default_status(scopedsession)
    return scopedsession


def create_default_status(session):
    ''' Insert default statues in status tables '''

    WEBSITES = APP.config['WEBSITES']
    SENTIMENT_SCORES = APP.config['SENTIMENT_SCORES']
    for website in WEBSITES:
        website_ = Website(website=website)
        session.add(website_)
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()

    for a in SENTIMENT_SCORES:
        sentiment, score = a[0], a[1]
        sentiment_ = Sentiment(sentiment=sentiment, score=score)
        session.add(sentiment_)
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()


def create_session(db_url, debug=False, pool_recycle=3600):
    ''' Create the Session object to use to query the database.
    :arg db_url: URL used to connect to the database. The URL contains
    information with regards to the database engine, the host to connect
    to, the user and password and the database name.
      ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg debug: a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a Session that can be used to query the database.
    '''
    engine = create_engine(
        db_url, echo=debug, pool_recycle=pool_recycle)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    BASE.metadata.bind = scopedsession
    return scopedsession


class Product(BASE):

    __tablename__ = 'products'

    token = sa.Column(sa.String(), nullable=False, primary_key=True)
    product_id = sa.Column(sa.String(), nullable=False)
    url = sa.Column(sa.Text(), nullable=False, unique=True)
    website_id = sa.Column(
                    sa.Integer,
                    sa.ForeignKey('websites.id'),
                    nullable=False)
    email = sa.Column(sa.Text(), nullable=False, default='female@email.com')
    bushy_positive_summary = sa.Column(sa.Text(), nullable=True, default='Empty')
    bushy_negative_summary= sa.Column(sa.Text(), nullable=True, default='Empty')
    gr_positive_summary = sa.Column(sa.Text(), nullable=True, default='Empty')
    gr_negative_summary= sa.Column(sa.Text(), nullable=True, default='Empty')

    sentiment_id = sa.Column( \
            sa.Integer,
            sa.ForeignKey('sentiments.id'),
            default=5,
            nullable=True)


class Website(BASE):

    __tablename__ = 'websites'

    id = sa.Column(sa.Integer, primary_key=True)
    website = sa.Column(sa.String(), unique=True, nullable=False)


class Sentiment(BASE):

    __tablename__ = 'sentiments'

    id = sa.Column(sa.Integer, primary_key=True)
    sentiment = sa.Column(sa.String(), unique=True, nullable=False)
    score = sa.Column(sa.Integer, nullable=False)


class Review(BASE):

    __tablename__ = 'reviews'

    id = sa.Column(sa.Integer, primary_key=True)
    product_token = sa.Column( \
                    sa.String(),
                    sa.ForeignKey('products.token'),
                    nullable=True)
    date = sa.Column(sa.String(), nullable=False, default=datetime.datetime.utcnow)
    is_verified = sa.Column(sa.Boolean, nullable=False, default=True)
    review = sa.Column(sa.Text(), nullable=False)
    sentiment_id = sa.Column( \
            sa.Integer,
            sa.ForeignKey('sentiments.id'),
            default=5,
            nullable=True)
