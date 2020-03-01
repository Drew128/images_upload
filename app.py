from flask import Flask, render_template, request, redirect, url_for, session
#import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
import math
from werkzeug.utils import secure_filename

"""from flask_login import current_user, login_user
from app.models import User

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)"""

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

@app.route('/script', methods=['GET', 'POST'])
def add_image_script():
    return render_template('add_image_script.js')


@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == "POST":
        print("filename", request.form.getlist('filename'))
        file = request.files['file']
        filename = secure_filename(file.filename)
        print("file", filename)
        print(type(file))
        new_image = Images(name=str(request.form.getlist('filename')[0]), link=f"http://link.net/image_n.img",
                           date=datetime.date.today())
        print(new_image.id,new_image.name, new_image.link, new_image.date)
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('image', image_id=new_image.id))
    return render_template('add_image.html')


@app.route('/image/change', methods=['GET', 'POST'])
def image_change():
    if request.method == "POST":
        form_id = request.form.getlist("#")[0]
        form_name = request.form.getlist("Name")[0]
        form_date = request.form.getlist("Date")[0]

        img = db.session.query(Images).get(form_id)              # suboptimal solution
        is_id = img.id == form_id
        is_name = img.name == form_name
        is_date = str(img.date) == str(form_date)
        print(is_date, img.date, form_date)
        if is_id and is_name and is_date:
            pass    # no change
        else:
            if not is_name:
                img.name = form_name
            if not is_date:
                img.date = datetime.date.today()
            print(db.session.commit())
        return redirect(url_for('image', image_id=form_id))


@app.route('/image/<int:image_id>', methods=['GET', 'POST'])
def image(image_id: int):
    page_id = get_page_number_by_img_number(image_id=image_id)
    return render_template('image.html', image_id=image_id, img=Images.query.get(image_id), page_id=page_id)


@app.route('/test', methods=['GET', 'POST'])
def test():
    obj = [[i, f"#image{i}", f"image{i}"] for i in range(10)]
    return render_template('test.html', obj=obj)

def get_page_number_by_img_number(per_page=app.config['ROWS_PER_PAGE'], image_id=1):
    page_id = (image_id-1)//per_page+1
    return page_id

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
        for i in range(1, 1000):
            db.session.add(Images(name=f"ImageName{i}", link=f"http://link.net/image{i}.img", date=datetime.datetime.now()))
        db.session.commit()
    app.run(debug=True)
