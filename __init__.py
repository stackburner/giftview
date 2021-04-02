from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Gift
from forms import GiftForm
from mailer import Mail
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
app = Flask(__name__)
app.config['SECRET_KEY'] = config['APP']['key']
app.config['DEBUG'] = config['APP']['debug']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB']['path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['APP']['track_modifications']
db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('gifts'))


@app.route('/new_gift', methods=['POST', 'GET'])
def new_gift():
    form = GiftForm()
    if form.validate_on_submit():
        my_gift = Gift()
        form.populate_obj(my_gift)
        db.session.add(my_gift)
        try:
            db.session.commit()
            flash('Gift created correctly', 'success')
            return redirect(url_for('gifts'))
        except Exception as e:
            db.session.rollback()
            flash('Error generating gift: {0}'.format(str(e)), 'danger')
    return render_template('web/new_gift.html', form=form)


@app.route('/edit_gift/<id>', methods=['POST', 'GET'])
def edit_gift(id):
    my_gift = Gift.query.filter_by(id=id).first()
    form = GiftForm(obj=my_gift)
    if form.validate_on_submit():
        try:
            form.populate_obj(my_gift)
            db.session.add(my_gift)
            db.session.commit()
            flash('Saved successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating gift: {0}'.format(str(e)), 'danger')
    return render_template('web/edit_gift.html', form=form)


@app.route('/gifts')
def gifts():
    all_gifts = Gift.query.order_by(Gift.name).all()
    return render_template('web/gifts.html', gifts=all_gifts)


@app.route('/gifts/delete', methods=['POST'])
def gifts_delete():
    try:
        my_gift = Gift.query.filter_by(id=request.form['id']).first()
        db.session.delete(my_gift)
        db.session.commit()
        Mail(config['MAIL']['server'],
             config['MAIL']['port'],
             config['MAIL']['user'],
             config['MAIL']['pw'],
             config['MAIL']['to'],
             config['MAIL']['sub'],
             config['MAIL']['message'].format(my_gift)).send()
        flash('Deleted successfully.', 'danger')

    except Exception as e:
        db.session.rollback()
        flash('Error deleting gift: {0}'.format(str(e)), 'danger')
    return redirect(url_for('gifts'))


if __name__ == '__main__':
    app.run()
