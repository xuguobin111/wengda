import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import EmailCpatchaModel,User
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20)])
    password = wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=6,max=6)])
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCpatchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower()!=captcha.lower():
            raise wtforms.ValidationError('验证码错误')
    def validate_email(self,field):
        email=field.data
        user_model = User.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经注册')
class LoginForms(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
class QuestionCheck(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=100)])
    content = wtforms.StringField(validators=[length(min=5)])
class Comment(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])




