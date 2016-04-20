#!/usr/bin/env python2

# These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.8', 'jinja2 >= 2.4']
import pkg_resources

from opinator import APP
from opinator.lib import models

models.create_tables(
    APP.config['SQLALCHEMY_DATABASE_URI'],
    debug=True
)
