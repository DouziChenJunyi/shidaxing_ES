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


def recruit_create_func():
    unit = request.form.get('unit')
    content = request.form.get('content')
    category = request.form.get('category')
    pay = request.form.get('pay')
    commend = request.form.get('commend')
    address = request.form.get('address')
    contact = request.form.get('contact')
    recruit = Recruit(unit=unit, content=content, category=category, pay=pay,
                      commend=commend, address=address, contact=contact)
    if request.form.get('remark'):
        remark = request.form.get('remark')
        recruit.remark = remark
    recruit.hasMoveIn = False
    return recruit

def recruit_select_func():
    if request.values.get('notSelect'):
        notSelect = request.values.get('notSelect')
    else:
        notSelect = "True"
    # 如果是查询
    if request.form.get('category'):
        recruit_category = request.form.get('category')
        session['category'] = recruit_category
        session.permanent = True
    # 如果是翻页
    else:
        recruit_category = session.get('category')
    # 如果input有值，即为一次查询
    if request.form.get('unit'):
        recruit_unit = request.form.get('unit')
        session['unit'] = recruit_unit
        session.permanent = True
    # 如果input无值
    else:
        # 如果是翻页
        if notSelect == "True":
            recruit_unit = session.get('unit')
        # 如果是一次查询，但input为空
        else:
            recruit_unit = ""
            session['unit'] = recruit_unit
        if recruit_unit == "none":
            recruit_unit = ""
    if recruit_category == "all":
        mode = 1
    elif recruit_category == "店员":
        mode = 2
    elif recruit_category == "家教":
        mode = 3
    else:
        mode = 4
    return mode, recruit_unit

def recruit_func(time, mode, recruit_unit="none"):
    if time == "history":
        hasMoveIn = False
    else:
        hasMoveIn = True
    if mode == "1":
        category = "none"
    elif mode == "2":
        category = "店员"
    elif mode == "3":
        category = "家教"
    else:
        category = "其他"
    page = request.args.get('page', 1, type=int)
    # 使用 es 读取数据
    pagination = query_recruit(hasMoveIn, recruit_unit, category, page)
    recruits = pagination.items

    ''' ------------ 使用 ORM 模型读取数据 ------------ '''
    '''
    if category == "none":
        if recruit_unit == "none":
            pagination = Recruit.query.filter(Recruit.hasMoveIn == hasMoveIn).order_by(
                Recruit.create_time.desc()).paginate(page,per_page=app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
        else:
            pagination = Recruit.query.filter(Recruit.hasMoveIn == hasMoveIn,Recruit.unit.contains(recruit_unit)).order_by(
                Recruit.create_time.desc()).paginate(page,per_page=app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    else:
        if recruit_unit == "none":
            pagination = Recruit.query.filter(Recruit.hasMoveIn == hasMoveIn,Recruit.category == category).order_by(
                Recruit.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
        else:
            pagination = Recruit.query.filter(Recruit.hasMoveIn == False,Recruit.category == category, Recruit.unit.contains(recruit_unit)).order_by(
                Recruit.create_time.desc()).paginate(page,per_page=app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)

    recruits = pagination.items
    '''
    return recruits, pagination
