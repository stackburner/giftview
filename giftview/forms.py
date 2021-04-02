from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
name_size = int(config['APP']['name_size'])
link_size = int(config['APP']['link_size'])
details_size = int(config['APP']['link_size'])


class GiftForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=name_size,
                                                  message='Only {0} characters allowed!'.format(name_size))])
    link = StringField('Link', validators=[DataRequired(), Length(min=-1, max=link_size,
                                                  message='Only {0} characters allowed!'.format(link_size))])
    details = StringField('Details', validators=[DataRequired(), Length(min=-1, max=details_size,
                                                        message='Only {0} characters allowed!'.format(details_size))])
