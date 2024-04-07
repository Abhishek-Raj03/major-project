from flask import Flask,redirect,url_for,render_template,request,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import json
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from mpl_toolkits import mplot3d
# from celluloid import Camera
from scipy import spatial
# import pyshine as ps
from calc_angle import calculateAngle,Average,convert_data,dif_compare,diff_compare_angle
from extract_keypoints import extractKeypoint
from compare_pose import compare_pose
from main import main
from dumble import dumb
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from pushup import push
from squats import squats_fun
import csv
import random
import subprocess
import threading
import webbrowser
import requests
from speed import speed1
# import id

# id=id
# id=0

class UploadFileForm(FlaskForm):
    file=FileField("File")
    submit=SubmitField("Upload File")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


app=Flask(__name__,static_url_path='',static_folder='./static')
app.secret_key = "secret key"

app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER']='static/video'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(20),nullable = False)
    age = db.Column(db.Integer(),nullable = False)


# class RegisterForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "User Name"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
#     confirm_password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Confirm Password"})
#     name = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Your name"})
#     age = IntegerField(validators=[
#                            InputRequired()], render_kw={"placeholder": "Age"})

#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(
#             username=username.data).first()
#         if existing_user_username:
#             raise ValidationError(
#                 'That username already exists. Please choose a different one.')

# class LoginForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')


@app.route('/')
def fun():
    return render_template('index.html')


# @app.route('/register',methods = ['POST','GET'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if form.password.data == form.confirm_password.data:
#             hashed_password = bcrypt.generate_password_hash(form.password.data)
#             new_user = User(username=form.username.data, password=hashed_password,name = form.name.data,age= form.age.data)
#             db.session.add(new_user)
#             db.session.commit()
#             return redirect(url_for('login'))
#         else:
#             return redirect(url_for('register'))

#     return render_template('register.html',form = form)

@app.route('/register_page')
def register_pager():
    return render_template('register.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_username = User.query.filter_by(
        username=request.form.get('username')).first()
        if existing_username:
            return redirect(url_for('login'))
        # if request.form.get('password') == "":
        #     return redirect(url_for('register'))
            
        if request.form.get('password') == request.form.get('confirm_password'):
            hashed_password = ""
            if request.form.get('password'):
                hashed_password = bcrypt.generate_password_hash(request.form.get('password'))
            else:
                return redirect(url_for('register'))
            name=request.form.get('name')
            password=request.form.get('password')
            username = request.form.get('username')
            age= request.form.get('age')
            gender= request.form.get('gender')
            csv_writer=csv.writer(open('users.csv','a',newline=""))
            df=pd.read_csv('users.csv')
            time_init=random.randint(2,20)
            cal_init=random.randint(10,100)
            a=[len(df)+1,name,username,password,age,gender,time_init,cal_init]
            csv_writer.writerow(a)
            new_user = User(username=request.form.get('username'), password=hashed_password,name = request.form.get('password'),age= request.form.get('age'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))


# @app.route('/login',methods = ['POST','GET'])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))

#     return render_template('login.html',form = form)
def find_index(input):
    with open('users.csv') as o:
        myData=csv.reader(o)
        for row in myData:
            if row[2]==input:
                return int(myData.line_num-1)
# id=0
@app.route('/login', methods=['GET', 'POST'])
def login():
    # global id
    if request.method == 'POST':
        user = User.query.filter_by(username= request.form.get('username')).first()
        if user:
            if bcrypt.check_password_hash(user.password, request.form.get('password')):
                login_user(user)
                # f=1
                # global id
                # id=id+find_index(request.form.get('username'))
                id1=find_index(request.form.get('username'))
                session['id']=id1
                # print(session.get('id'))
                # localStorage
                # id=id.MyClass(ide=id1)
                # id.ide.id=id1

                # id=int(id)
                # id=id-1
                # print("-----------------------"+str(id)+"--------------------")
                return redirect(url_for('features'))
                # return redirect(url_for('dashboard'))

        
            
    return render_template('login.html',title = 'Login')




@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    flash("Logged in")
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/features')
@login_required
def features():
    # category = 'fitness'
    # api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    # response = requests.get(api_url, headers={'X-Api-Key': 'eQTly/BTtC/bl6t3APTDSg==zGUXnjnEXYfOkAnI'})
    # # if response.status_code == requests.codes.ok:
    # #     print(response.text)
    # # else:
    # #     print("Error:", response.status_code, response.text)
    # s = response.text

    # # Parse the JSON string
    # data = json.loads(s)

    # # Access the values using keys
    # quote = data[0]['quote']
    # author = data[0]['author']
    # category = data[0]['category']
    quote="I think exercise tests us in so many ways, our skills, our hearts, our ability to bounce back after setbacks. This is the inner beauty of sports and competition, and it can serve us all well as adult athletes."
    author="Peggy Fleming"
    return render_template('feature.html',quote=quote,author=author)

@app.route('/yogaMain',methods=['GET','POST'])
@login_required
def yogaMain():
    form=UploadFileForm()
    if form.validate_on_submit():
        file=form.file.data # grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # save the file
        main(file.filename)
        os.remove("static/video/"+file.filename)
        return redirect(url_for('yogaMain'))
    else:
        return render_template('yogaMain.html',form=form)


@app.route('/pose/<id>')
def pose(id):
    ide=session.get('id')
    # referrer=request.headers.get('Referer')
    main(id,ide)
    return redirect(url_for('yogaMain'))
    # return redirect(referrer)

@app.route('/gym')
def gym():
    return render_template('gym.html')

@app.route('/dumble')
def dumble():
    id=session.get('id')
    # print("-----------------"+str(id)+"-----------------")
    dumb(id)
    return redirect(url_for('gym'))

@app.route('/pushup')
def pushup():
    id=session.get('id')
    push(id)
    return redirect(url_for('gym'))

@app.route('/squats')
def squats():
    id=session.get('id')
    squats_fun(id)
    return redirect(url_for('gym'))

@app.route('/speed')
def speed():
    speed1()
    return redirect(url_for('features'))

@app.route('/feedback')
def feedback():
    # print("---------------------------")
    csv_reader=csv.reader(open('feedback.csv','r',newline=""))
    lis=list(csv_reader)
    lis=lis[1:]
    r=0
    for i in lis:
        a=i[2]
        a=int(a)
        r=r+int(a)
    r=r/len(lis)
    return render_template('feedback.html',df=lis,r=r)

@app.route('/feed',methods=['GET','POST'])
def feed():
    star=0
    review=request.form.get('review')
    star=int(request.form['rate'])
    id=session.get('id')
    df=pd.read_csv('users.csv')
    df1=pd.read_csv('feedback.csv')
    num_row=-1
    c=0
    with open('feedback.csv', 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if(str(row[0])==str(id)):
               num_row=c
               break
            c+=1
    num_row-=1
    print(review)
    if(num_row<0):
        csv_writer=csv.writer(open('feedback.csv','a',newline=""))
        lis=[id,df.loc[id-1,'name'],star,review]
        csv_writer.writerow(lis)
        print('Inside first')
    else:
        df1.loc[num_row,'star']=star
        df1.loc[num_row,'review']=review
        df1.to_csv('feedback.csv',index=False)
    return redirect(url_for('feedback'))

def run_streamlit_server():
    # Replace 'your_streamlit_script.py' with the name of your Streamlit script
    subprocess.run(['python','-m','streamlit', 'run', 'dashboard.py'])

def run_mailer_script():
    print('------mailer------------------')
    # Replace 'mailer.py' with the name of your mailer script
    subprocess.Popen(['python','mailer.py'])
@app.route('/start_streamlit')
def start_streamlit():
    # Start Streamlit server in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit_server)
    streamlit_thread.start()
    # subprocess.run(['python','-m','streamlit', 'run', 'dashboard.py'])

    # mailer_thread = threading.Thread(target=run_mailer_script)
    # mailer_thread.start()
    # subprocess.run(['python','mailer.py'])
    # run_streamlit_server()

    # Open a new browser window or tab to the Streamlit app
    # webbrowser.open('http://localhost:8501')

    return redirect(url_for('features'))

if __name__ == '__main__':
    app.run(debug=True)