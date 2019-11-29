from flask import Flask, render_template, request, redirect, url_for, session
#import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
import math
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///example.sqlite"
app.config['ROWS_PER_PAGE'] = 10
db = SQLAlchemy(app)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


@app.route('/')
def index():
    return redirect(url_for('images_list', page_id=1))

@app.route('/images_list/page/<int:page_id>', methods=['GET', 'POST'])
def images_list(page_id: int):
    if page_id < 1:
        return redirect(url_for('index', page_id=1))
    last_page = get_image_pages_count()
    if page_id > last_page:
        return redirect(url_for('index', page_id=last_page))
    return render_template('images_list.html', get_image_list=get_image_list, last_page=last_page, page_id=page_id)

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == "POST":
        print("filename", request.form.getlist('filename'))
        file = request.files['file']
        filename = secure_filename(file.filename)
        print("file", filename)
        print(type(file))
    return render_template('add_image.html')

def get_image_list(per_page=app.config['ROWS_PER_PAGE'], page_id=1):
    page_id -= 1                            # to make indexes starts with 1 instead of 0
    images = Images.query.limit(per_page).offset(page_id*per_page).all()
    return images

def get_image_pages_count(per_page=app.config['ROWS_PER_PAGE']):
    images = Images.query.count()
    pages = math.ceil(images/per_page)
    return pages


if __name__ == '__main__':
    try:
        Images.query.count()
    except Exception:
        db.create_all()
        for i in range(1, 100):
            db.session.add(Images(name=f"ImageName{i}", link=f"http://link.net/image{i}.img", date=datetime.datetime.now()))
        db.session.commit()
        images = Images.query.all()
        print(images)
    app.run(debug=True)
