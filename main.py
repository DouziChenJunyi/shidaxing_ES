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

from tenement_api import *
from recruit_api import *
from databse_to_es import write_tenement_elasticsearch, write_recruit_elasticsearch

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=3600)
app.config.from_object(config)
app.config['DEBUG'] = True
db.init_app(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def index():
    # write_tenement_elasticsearch()
    # write_recruit_elasticsearch()
    if request.method == 'GET':
        return render_template('index.html')
    else:
        state = login_func()
        if state:
            return redirect(url_for('tenement_select_current'))
        else:
            return render_template('_login_fail.html')



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('_login.html')
    else:
        state = login_func()
        if state:
            return redirect(url_for('tenement_select_current'))
        else:
            return render_template('_login_fail.html')


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('_register.html')
    else:
        state, fail_info = register_func()
        if state == 1:
            return render_template('_register_fail.html', fail=fail_info)
        elif state == 2:
            return render_template('_register_fail.html', fail=fail_info)
        elif state == 3:
            return render_template('_register_fail.html', fail=fail_info)
        else:
            return redirect(url_for('login'))



@app.route('/modify_username/<user_id>',methods=['GET','POST'])
def modify_username(user_id):
    if request.method == 'GET':
        return render_template('modify_username.html')
    else:
        state = modify_username_func(user_id)
        if (state):
            return redirect(url_for('login'))
        else:
            return render_template('test_username_fail.html')


@app.route('/modify_password/<user_id>',methods=['GET','POST'])
def modify_password(user_id):
    if request.method == 'GET':
        return render_template('modify_password.html')
    else:
        state = modify_password_func(user_id)
        if state == 1:
            return redirect(url_for('login'))
        else:
            return render_template('test_password_fail.html')


@app.route('/modify_signal/<user_id>',methods=['GET','POST'])
def modify_signal(user_id):
    if request.method == 'GET':
        return render_template('modify_signal.html')
    else:
        state = modify_signal_func(user_id)
        if state == True:
            return render_template('test_signal_fail.html')
        else:
            return redirect(url_for('login'))

@app.route('/_show_managers/')
def _show_managers():
    page = request.args.get('page', 1, type=int)
    if User.query.order_by(User.create_time.desc()).paginate(page, per_page=  app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False):
        pagination = User.query.order_by(User.create_time.desc()).paginate(page, per_page=app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    else:
        pagination = User.query.filter().all().paginate(page, per_page=
        app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    users = pagination.items
    return render_template('_show_managers.html', users=users,
                           pagination=pagination)


@app.route('/_managers_delete/<user_id>/')
def _managers_delete(user_id):
    user_model = User.query.filter(User.id == user_id).first()
    db.session.delete(user_model)
    db.session.commit()
    return redirect(url_for("_show_managers"))



@app.route('/link_tenement_current/')
def link_tenement_current():
    session['price'] = 'all'
    session['name'] = "none"
    session.permanent = True
    return redirect(url_for('tenement_select_current'))


@app.route('/tenement_select_current/',methods=['GET','POST'])
def tenement_select_current():
    page = request.args.get('page', 1, type=int)
    mode, tenement_name = tenement_select_func()
    if tenement_name == "":
        return redirect(url_for('tenement', time="current", mode=mode, page=page, tenement_name="none"))
    else:
        return redirect(url_for('tenement', time="current", mode=mode, tenement_name=tenement_name,page=page))


@app.route('/link_tenement_history/')
def link_tenement_history():
    session['price'] = 'all'
    session['name'] = "none"
    session.permanent = True
    return redirect(url_for('tenement_select_history'))


@app.route('/tenement_select_history/',methods=['GET','POST'])
def tenement_select_history():
    page = request.args.get('page', 1, type=int)
    mode, tenement_name = tenement_select_func()
    if tenement_name == "":
        return redirect(url_for('tenement', time="history", mode=mode, page=page, tenement_name="none"))
    else:
        return redirect(url_for('tenement', time="history", mode=mode, page=page,tenement_name=tenement_name))


@app.route('/tenement/<time>/<mode>/<tenement_name>')
@login_required
def tenement(time, mode, tenement_name="none"):
    tenements, pagination = tenement_func(time, mode, tenement_name)
    if time == "history":
        return render_template('tenement_info_history.html', tenements=tenements,pagination=pagination)
    else:
        return render_template('tenement_info_current.html', tenements=tenements, pagination=pagination)



@app.route('/tenement_table_create/',methods=['GET', 'POST'])
def tenement_table_create():
    if request.method == 'GET':
        return render_template('tenement_table_create.html')
    else:
        tenement = tenement_table_create_func()
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_list = ["file1", "file2", "file3", "file4", "file5", "file6"]
        for file in file_list:
            # noinspection PyBroadException
            try:
                f = request.files[file]
                if not (f and allowed_file(f.filename)):
                    return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
                file_path = secure_filename(f.filename)
                # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                upload_path1 = os.path.join(basepath, 'static/upload_images', file_path)
                f.save(upload_path1)
                # 使用Opencv转换一下图片格式和名称
                img = cv2.imread(upload_path1)
                cv2.imwrite(os.path.join(basepath, 'static/upload_images', file_path), img)
                tenement = save_file(file, tenement, file_path)
            except Exception as e:
                tenement = save_file(file, tenement)
            db.session.add(tenement)
            db.session.commit()
            return redirect(url_for("tenement_select_current"))


@app.route('/tenement_item_check/<tenement_id>/')
def tenement_item_check(tenement_id):
    tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
    return render_template('tenement_item_check.html', tenement=tenement_model)


@app.route('/tenement_item_modify/<tenement_id>/',methods=['GET','POST'])
def tenement_item_modify(tenement_id):
    if request.method == 'GET':
        tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
        return render_template('tenement_item_modify.html',tenement=tenement_model)
    else:
        tenement_model = tenement_item_modify_func(tenement_id)
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        file_list = ["file1", "file2", "file3", "file4", "file5", "file6"]
        for file in file_list:
            # noinspection PyBroadException
            try:
                f = request.files['file']
                if not (f and allowed_file(f.filename)):
                    return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
                file_path = secure_filename(f.filename)
                upload_path = os.path.join(basepath, 'static/upload_images', file_path)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                f.save(upload_path)
                # 使用Opencv转换一下图片格式和名称
                img = cv2.imread(upload_path)
                if os.path.exists(PATH_BEFORE + tenement_model.image1):
                    os.remove(PATH_BEFORE + tenement_model.image1)
                cv2.imwrite(os.path.join(basepath, 'static/upload_images', file_path), img)
                tenement_model = save_file(file, tenement_model, file_path)
            except Exception as e:
                tenement_model = save_file(file, tenement_model, tenement_model.image1)
        db.session.commit()
        return redirect(url_for("tenement_select_history"))


@app.route('/tenement_item_delete/<tenement_id>/')
def tenement_item_delete(tenement_id):
    tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
    db.session.delete(tenement_model)
    db.session.commit()
    return redirect(url_for("tenement_select_history"))


@app.route('/tenement_item_moveIn/<tenement_id>/',methods=['GET','POST'])
def tenement_item_moveIn(tenement_id):
    tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
    tenement_model.hasMoveIn = True
    db.session.commit()
    return redirect(url_for("tenement_select_history"))


@app.route('/tenement_item_moveOut/<tenement_id>/',methods=['GET','POST'])
def tenement_item_moveOut(tenement_id):
    tenement_model = Tenement.query.filter(Tenement.id == tenement_id).first()
    tenement_model.hasMoveIn = False
    db.session.commit()
    return redirect(url_for("tenement_select_current"))


@app.route('/recruit_table_create/',methods=['GET', 'POST'])
def recruit_table_create():
    if request.method == 'GET':
        return render_template('recruit_table_create.html')
    else:
        recruit = recruit_create_func()
        db.session.add(recruit)
        db.session.commit()
        return redirect(url_for("recruit_info_current"))


@app.route('/recruit_item_check/<recruit_id>/')
def recruit_item_check(recruit_id):
    recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
    return render_template('recruit_item_check.html',recruit=recruit_model)


@app.route('/link_recruit_current/')
def link_recruit_current():
    session['category'] = 'all'
    session['unit'] = "none"
    session.permanent = True
    return redirect(url_for('recruit_select_current'))


@app.route('/recruit_select_current/',methods=['GET','POST'])
def recruit_select_current():
    # page = request.args.get('page', 1, type=int)
    mode, recruit_unit = recruit_select_func()
    if recruit_unit == "":
        return redirect(url_for('recruit', time="current", mode=mode, recruit_unit="none"))
    else:
        return redirect(url_for('recruit', time="current", mode=mode, recruit_unit=recruit_unit))


@app.route('/link_recruit_history/')
@login_required
def link_recruit_history():
    session['category'] = 'all'
    session['unit'] = "none"
    session.permanent = True
    return redirect(url_for('recruit_select_history'))


@app.route('/recruit_select_history/',methods=['GET', 'POST'])
def recruit_select_history():
    mode, recruit_unit = recruit_select_func()
    if recruit_unit == "":
        return redirect(url_for('recruit', time="history", mode=mode,  recruit_unit="none"))
    else:
        return redirect(url_for('recruit', time="history", mode=mode, recruit_unit=recruit_unit))


@app.route('/recruit/<time>/<mode>/<recruit_unit>')
@login_required
def recruit(time, mode, recruit_unit="none"):
    recruits, pagination = recruit_func(time, mode, recruit_unit)
    if time == "history":
        return render_template('recruit_info_history.html', recruits=recruits,
                               pagination=pagination)
    else:
        return render_template('recruit_info_current.html', recruits=recruits,
                               pagination=pagination)


@app.route('/recruit_item_modify/<recruit_id>/',methods=['GET','POST'])
def recruit_item_modify(recruit_id):
    if request.method == 'GET':
        recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
        return render_template('recruit_item_modify.html',recruit=recruit_model)
    else:
        recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
        recruit_model.unit = request.form.get('unit')
        recruit_model.content = request.form.get('content')
        recruit_model.pay = request.form.get('pay')
        recruit_model.commend = request.form.get('commend')
        recruit_model.address = request.form.get('address')
        recruit_model.contact = request.form.get('contact')
        recruit_model.remark = request.form.get('remark')
        recruit_model.category = request.form.get('category')
        db.session.commit()
        return redirect(url_for('link_recruit_history'))


@app.route('/recruit_item_delete/<recruit_id>/')
def recruit_item_delete(recruit_id):
    recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
    db.session.delete(recruit_model)
    db.session.commit()
    return redirect(url_for("link_recruit_history"))


@app.route('/recruit_item_moveIn/<recruit_id>/',methods=['GET','POST'])
def recruit_item_moveIn(recruit_id):
    recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
    recruit_model.hasMoveIn = True
    db.session.commit()
    return redirect(url_for("link_recruit_history"))


@app.route('/recruit_info_current/')
@login_required
def recruit_info_current():
    page = request.args.get('page', 1, type=int)
    pagination = Recruit.query.filter(Recruit.hasMoveIn == True).order_by(
        Recruit.create_time.desc()).paginate(page, per_page=
    app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    recruits = pagination.items
    return render_template('recruit_info_current.html', recruits=recruits,
                           pagination=pagination)


@app.route('/recruit_item_moveOut/<recruit_id>/',methods=['GET','POST'])
def recruit_item_moveOut(recruit_id):
    recruit_model = Recruit.query.filter(Recruit.id == recruit_id).first()
    recruit_model.hasMoveIn = False
    db.session.commit()
    return redirect(url_for("recruit_info_current"))



@app.route('/__tenement_list_low/')
def __tenement_list_low():
    context = {
        'tenements': Tenement.query.filter(Tenement.hasMoveIn == True,
                                           Tenement.price == '300-450').order_by(
            Tenement.create_time.desc()).all()
    }
    return render_template('__tenement_list_low.html', **context)


@app.route('/__tenement_list_middle/')
def __tenement_list_middle():
    context = {
        'tenements': Tenement.query.filter(Tenement.hasMoveIn == True,
                                           Tenement.price == '450-700').order_by(
            Tenement.create_time.desc()).all()
    }
    return render_template('__tenement_list_middle.html', **context)


@app.route('/__tenement_list_high/')
def __tenement_list_high():
    context = {
        'tenements': Tenement.query.filter(Tenement.hasMoveIn == True,
                                           Tenement.price == '700+').order_by(
            Tenement.create_time.desc()).all()
    }
    return render_template('__tenement_list_high.html', **context)


@app.route('/__tenement_detail/<tenement_id>')
def __tenement_detail(tenement_id):
    tenement = Tenement.query.filter(Tenement.id == tenement_id).first()
    return render_template('__tenement_detail.html',tenement=tenement)


@app.route('/__tenement_photoes/<tenement_id>')
def __tenement_photoes(tenement_id):
    tenement = Tenement.query.filter(Tenement.id == tenement_id).first()
    return render_template('__tenement_photoes.html',tenement=tenement)


@app.route('/__recruit_list_all/')
def __recruit_list_all():
    context = {
        'recruits': Recruit.query.filter(Recruit.hasMoveIn == True).order_by(
            Recruit.create_time.desc()).all()
    }
    return render_template('__recruit_list_all.html', **context)


@app.route('/__recruit_list_tutor/')
def __recruit_list_tutor():
    context = {
        'recruits': Recruit.query.filter(Recruit.hasMoveIn == True,
                                         Recruit.category == '家教').order_by(
            Recruit.create_time.desc()).all()
    }
    return render_template('__recruit_list_tutor.html', **context)


@app.route('/__recruit_list_waitor/')
def __recruit_list_waitor():
    context = {
        'recruits': Recruit.query.filter(Recruit.hasMoveIn == True,
                                         Recruit.category == '店员').order_by(
            Recruit.create_time.desc()).all()
    }
    return render_template('__recruit_list_waitor.html', **context)


@app.route('/__recruit_list_other/')
def __recruit_list_other():
    context = {
        'recruits': Recruit.query.filter(Recruit.hasMoveIn == True,
                                         Recruit.category == '其他').order_by(
            Recruit.create_time.desc()).all()
    }
    return render_template('__recruit_list_other.html', **context)


@app.context_processor
def my_context_processor():
    boss = Boss.query.filter(Boss.id == 1).first()
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user, 'boss': boss}
    else:
        return {}


if __name__ == '__main__':
    app.run(host="127.0.0.1",debug=True)