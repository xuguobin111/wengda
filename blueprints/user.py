from flask import Blueprint,render_template,request,redirect,url_for,jsonify,session,flash
from exts import mail,db
from flask_mail import Message
from models import EmailCpatchaModel,User
import string
import random
from datetime import datetime
from blueprints.forms import RegisterForm,LoginForms
from werkzeug.security import generate_password_hash,check_password_hash
bp = Blueprint('user',__name__,url_prefix='/user')
@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForms(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password,password):
                session['user_id']=user.id
                return redirect('/')
            else:
                flash('邮箱或密码不匹配')
                return redirect(url_for('user.login'))
        else:
            flash('邮箱或密码格式错误')
            return redirect(url_for('user.login'))


@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)
            user = User(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))
@bp.route('/captcha',methods=['POST'])
def get_captcha():
    email = request.form.get('email')
    letters = string.ascii_letters+string.digits
    captcha = "".join(random.sample(letters,6))
    if email:
        message = Message(
            subject='邮箱测试',
            recipients=[email],
            body=f'[知乎问答]您的注册验证码是：{captcha}'
             )
        mail.send(message)
        captcha_model = EmailCpatchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha=captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCpatchaModel(email=email,captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print('captcha:',captcha)
        return jsonify({'code':200})
    else:
        return jsonify({'code':400,'message':'请先传递邮箱！'})
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))