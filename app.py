from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
import math


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///example.sqlite"
app.config['ROWS_PER_PAGE'] = 4
db = SQLAlchemy(app)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/page/<int:page_id>', methods=['GET', 'POST'])
def index(page_id: int):
    if page_id < 1:
        return redirect(url_for('index', page_id=1))
    last_page = get_image_pages_count()
    if page_id > last_page:
        return redirect(url_for('index', page_id=last_page))
    return render_template('index.html', get_image_list=get_image_list, last_page=last_page, page_id=page_id)

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    return render_template('add_image.html')

@app.route('/page/', methods=['GET', 'POST'])
def page_no_par():
    return redirect(url_for('index', page_id=1))


def get_image_list(per_page=app.config['ROWS_PER_PAGE'], page_id=1):
    page_id -= 1                            # to make indexes starts with 1 instead of 0
    images = Images.query.limit(per_page).offset(page_id*per_page).all()
    return images

def get_image_pages_count(per_page=app.config['ROWS_PER_PAGE']):
    images = Images.query.count()
    pages = math.ceil(images/per_page)
    return pages


if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()
    # for i in range(1, 10):
    #     db.session.add(Images(name=f"ImageName{i}", link=f"http://link.net/image{i}.img", date=datetime.datetime.now()))
    # db.session.commit()
    #
    # users = Images.query.all()
    # print(users)