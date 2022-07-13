#encoding: utf-8
from flask import Flask,render_template,request,session,redirect,url_for,make_response, jsonify
from models import Boss,User,Tenement,Recruit
from werkzeug.utils import secure_filename
from decorators import login_required
from datetime import timedelta
from exts import db
from config import PATH_BEFORE

import config
import cv2
import os
from elasticsearch_api import *

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=3600)
app.config.from_object(config)
app.config['DEBUG'] = True
db.init_app(app)


def login_func():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    if user:
        session['user_id'] = user.id
        session['price'] = 'all'
        session['name'] = "none"
        session['category'] = "all"
        session['unit'] = "none"

        session.permanent = True
        return True
    else:
        return False

def modify_username_func(user_id):
    user = User.query.filter(User.id == user_id).first()
    boss = Boss.query.filter(Boss.id == 1).first()
    user_pwd = user.password
    username = request.form.get('username')
    password = request.form.get('password')
    if password == user_pwd:
        if user.username == boss.username and user.password == boss.password:
            boss.username = username
        user.username = username
        db.session.commit()
        session.pop('user_id')
        return True
    else:
        session.pop('user_id')
        return False

def register_func():
    username = request.form.get('username')
    signal = request.form.get('signal')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user = User.query.filter(User.username == username).first()
    if user:
        fail = "username"
        return 1, fail
    else:
        if password1 != password2:
            fail = "password"
            return 2, fail
        elif signal != Boss.query.filter(Boss.id == 1).first().signal:
            fail = "signal"
            return 3, fail
        else:
            user = User(username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return 4, ""

def modify_password_func(user_id):
    user = User.query.filter(User.id == user_id).first()
    boss = Boss.query.filter(Boss.id == 1).first()
    user_pwd = user.password
    password_cur = request.form.get('password_cur')
    password_new = request.form.get('password_new')
    if password_cur == user_pwd:
        if user.username == boss.username and user.password == boss.password:
            boss.password = password_new
        user.password = password_new
        db.session.commit()
        session.pop('user_id')
        return True
    else:
        session.pop('user_id')
        return False

def modify_signal_func(user_id):
    user = User.query.filter(User.id == user_id).first()
    boss = Boss.query.filter(Boss.id == 1).first()
    password = user.password
    signal_cur = request.form.get('signal_cur')
    signal_new = request.form.get('signal_new')
    if password != user.password or signal_cur != boss.signal:
        session.pop('user_id')
        return True
    else:
        boss.signal = signal_new
        db.session.commit()
        session.pop('user_id')
        return False

def tenement_select_func():
    # 提交表单传的False是str类型
    if request.values.get('notSelect'):
        notSelect = request.values.get('notSelect')
    # 无法获取参数（说明是首次进入），此时不是查询
    else:
        notSelect = "True"
    if request.form.get('price'):
        tenement_price = request.form.get('price')
        session['price'] = tenement_price
        session.permanent = True
    else:
        tenement_price = session.get('price')
    if request.form.get('name'):
        tenement_name = request.form.get('name')
        session['name'] = tenement_name
        session.permanent = True
    else:
        # 不是查询（两种情况，重定向或翻页）
        if notSelect == "True":
            tenement_name = session.get('name')
        # 是查询，但是是无Input值查询
        else:
            tenement_name = ""
            session['name'] = tenement_name
        if tenement_name == "none":
            tenement_name = ""
    if tenement_price == "all":
        mode = 1
    elif tenement_price == "300-450":
        mode = 2
    elif tenement_price == "450-700":
        mode = 3
    else:
        mode = 4
    return mode, tenement_name


def tenement_func(time, mode, tenement_name="none"):
    if time == "history":
        hasMoveIn = False
    else:
        hasMoveIn = True
    if mode == "1":
        price = "none"
    elif mode == "2":
        price = "300-450"
    elif mode == "3":
        price = "450-700"
    else:
        price = "700+"
    page = request.args.get('page', 1, type=int)
    # 使用 es 读取数据
    pagination = query_tenement(hasMoveIn, tenement_name, price, page)
    tenements = pagination.items
    ''' ------------- 使用 ORM 模型读数据 ---------- '''
    '''
    if price == "none":
        if tenement_name == "none":
            pagination = Tenement.query.filter(Tenement.hasMoveIn == hasMoveIn).order_by(
                    Tenement.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
        else:
            pagination = Tenement.query.filter(Tenement.hasMoveIn == hasMoveIn,
                                               Tenement.flat_name.contains(tenement_name)).order_by(
                    Tenement.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    else:
        if tenement_name == "none":
            pagination = Tenement.query.filter(Tenement.hasMoveIn == hasMoveIn, Tenement.price == price).order_by(
                Tenement.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
        else:
            pagination = Tenement.query.filter(Tenement.hasMoveIn == hasMoveIn,Tenement.price == price,
                                               Tenement.flat_name.contains(tenement_name)).order_by(
                Tenement.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    tenements = pagination.items
    '''
    return tenements, pagination


def tenement_table_create_func():
    flat_name = request.form.get('flat_name')
    flat_id = request.form.get('flat_id')
    room_count = request.form.get('room_count')
    bathroom_count = request.form.get('bathroom_count')
    price = request.form.get('price')
    deposit = request.form.get('deposit')
    telephone1 = request.form.get('telephone1')
    address = request.form.get('address')
    tenement = Tenement(flat_name=flat_name, room_count=room_count,
                        bathroom_count=bathroom_count, price=price,
                        deposit=deposit, telephone1=telephone1, address=address)
    tenement.flat_id = "http://j.map.baidu.com/" + flat_id
    if request.form.get('kitchen_count'):
        kitchen_count = request.form.get('kitchen_count')
        tenement.kitchen_count = kitchen_count
    else:
        tenement.kitchen_count = 0
    if request.form.get('livingroom_count'):
        livingroom_count = request.form.get('livingroom_count')
        tenement.livingroom_count = livingroom_count
    else:
        tenement.livingroom_count = 0
    if request.form.get('telephone2'):
        telephone2 = request.form.get('telephone2')
        tenement.telephone2 = telephone2
    # else:
    #     tenement.telephone2 = "none"
    if request.form.get('remark'):
        remark = request.form.get('remark')
        tenement.remark = remark
    if request.form.get('kitchen'):
        tenement.kitchen = 'True'
    else:
        tenement.kitchen = 'False'
    if request.form.get('window'):
        tenement.window = 'True'
    else:
        tenement.window = 'False'
    if request.form.get('lift'):
        tenement.lift = 'True'
    else:
        tenement.lift = 'False'
    tenement.hasMoveIn = True
    return tenement


def save_file(file, tenement, file_path="none"):
    if file == "file1":
        tenement.image1 = file_path
    elif file == "file2":
        tenement.image2 = file_path
    elif file == "file3":
        tenement.image3 = file_path
    elif file == "file4":
        tenement.image4 = file_path
    elif file == "file5":
        tenement.image5 = file_path
    else:
        tenement.image6 = file_path
    return tenement

def tenement_item_modify_func(tenement_id):
    tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
    tenement_model.flat_name = request.form.get('flat_name')
    tenement_model.flat_id = request.form.get('flat_id')
    tenement_model.room_count = request.form.get('room_count')
    tenement_model.bathroom_count = request.form.get('bathroom_count')
    tenement_model.price = request.form.get('price')
    tenement_model.deposit = request.form.get('deposit')
    tenement_model.telephone1 = request.form.get('telephone1')
    tenement_model.address = request.form.get('address')
    if request.form.get('kitchen'):
        tenement_model.kitchen = 'True'
    else:
        tenement_model.kitchen = 'False'
    if request.form.get('window'):
        tenement_model.window = 'True'
    else:
        tenement_model.window = 'False'
    if request.form.get('lift'):
        tenement_model.lift = 'True'
    else:
        tenement_model.lift = 'False'
    return tenement_model