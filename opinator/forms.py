from flask.ext import wtf
import wtforms

class RequestForm(wtf.Form):
    ''' Form to validate the input from the plugin '''

    product_id = wtforms.TextField('Product ID',
                                [wtforms.validators.Required()])
    url = wtforms.TextField('URL',
                                [wtforms.validators.Required()])
    website = wtforms.TextField('Website',
                                [wtforms.validators.Required()])
    email = wtforms.TextField('Email',
                                [wtforms.validators.Email()])
