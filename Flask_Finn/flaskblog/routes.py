
import os
import secrets
from PIL import Image
from flask import render_template,url_for, flash, redirect, request, abort,send_from_directory
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User,Post,Jobb
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.finn_jobb import scraping
import pandas as pd
from sqlalchemy.sql import text
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from threading import Timer
import sys



@app.route("/",methods=['GET', 'POST'])
@login_required
def hello():
    surveys_df = pd.read_sql_query("SELECT * from jobb", con=db.engine)
    new_df = surveys_df[surveys_df['user_id'] == current_user.id]
    new_df = new_df.drop(columns=['user_id'])
    return render_template('table.html',tables=[new_df.to_html(classes='table table-dark table-striped table-sm',header="true",index=False,justify='left')],titles=new_df.columns.values,current_user=current_user)


@app.route("/home")
def home():
    surveys_df = pd.read_sql_query("SELECT * from jobb", con=db.engine)
    new_df = surveys_df[surveys_df['user_id'] == current_user.id]
    new_df = new_df.drop(columns=['user_id'])
    return render_template('table.html',tables=[new_df.to_html(classes='table table-dark table-striped table-sm',header="true",index=False,justify='left')],titles=new_df.columns.values,current_user=current_user)





@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('account updated.','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data= current_user.email
    image_file=url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',image_file=image_file, form=form)


@app.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #post = Post(title=form.title.data, content=form.content.data, author=current_user)
        content=form.content.data
        content_split= content.split()
        content_html_table = scraping(content_split)
        content_test = content_html_table.to_html(classes='table table-striped',header="true",index=False)
        content_html_table['user_id']=[current_user.id for n in range(len(content_html_table.index))]

        content_html_table.to_sql(name='jobb', con=db.engine, index=False,if_exists='append')
        db.session.commit()
        flash('new post','success')
        return render_template('table.html',tables=[content_html_table.to_html(classes='table table-striped',header="true",index=False)],titles=content_html_table.columns.values)
        
        #return redirect(url_for('home'))
    return render_template('create_post.html',title='New post', form=form, legend='New Post')




@app.route("/update_jobb",methods=['GET', 'POST'])
@login_required
def update_jobs():
    
    jobs_ = pd.read_sql_query("SELECT * from jobb", con=db.engine)
    jobs_ = jobs_[jobs_['user_id'] == current_user.id]
    jobs_url = jobs_
    jobs_url['user_id']=[current_user.id for n in range(len(jobs_url.index))]
    jobs_url = jobs_url['url']
    jobs_url = [item for item in jobs_url]
    jobs_test = ""
    for item in jobs_url:
        jobs_test = jobs_test + item +'\n'

    form = PostForm()
    if form.validate_on_submit():
        
        content=form.content.data
        content_split= content.split()
        content_html_table = scraping(content_split)
        content_html_table['user_id']=[current_user.id for n in range(len(content_html_table.index))]
        test = content_html_table
        test = test.drop_duplicates()
        
        db.engine.execute(text(f"DELETE from jobb WHERE user_id={current_user.id}"))
        db.session.commit()
        test.to_sql(name='jobb', con=db.engine, index=False,if_exists='append')
        
        db.session.commit()
        flash(f'{content_split}','success')
        return redirect('/')
    elif request.method == 'GET':
        form.content.data = jobs_test
    return render_template('create_post.html',title='Update Post', form=form, legend='Update Post')




@app.route("/save_file")
@login_required
def send_it():
    file = 'static/test.txt'
    return send_from_directory(directory='static',filename='bg.jpg', as_attachment=True)

