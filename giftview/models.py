from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']['path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['APP']['track_modifications']
db = SQLAlchemy(app)


class Gift(db.Model):
    __tablename__ = 'gifts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(config['APP']['name_size']), nullable=False)
    link = db.Column(db.String(config['APP']['link_size']), nullable=False)
    details = db.Column(db.String(config['APP']['details_size']), nullable=False)

    def __repr__(self):
        return '<Gifts %r>' % self.name
