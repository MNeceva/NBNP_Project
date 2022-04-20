from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, Length, AnyOf
from app.models import Users

class LoginForm(FlaskForm):
    email_login = StringField("ЕЛЕКТРОНСКА АДРЕСА: ", validators=[DataRequired(), Email()])
    password_login = PasswordField("ЛОЗИНКА: ", validators=[DataRequired()])
    remember_me = BooleanField('Остани најавен', default=False, validators=[AnyOf([True, False])])
    login_btn = SubmitField("НАЈАВИ СЕ")


class RegisterForm(FlaskForm):
    firstname = StringField("ИМЕ: ", validators=[DataRequired()])
    lastname = StringField("ПРЕЗИМЕ: ", validators=[DataRequired()])
    username = StringField("KОРИСНИЧКО ИМЕ: ", validators=[DataRequired(),
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                'Usernames must have only letters, numbers, dots or '
                                                'underscores')])
    password = PasswordField("ЛОЗИНКА: ", validators=[DataRequired()])
    email = EmailField("ЕЛЕКТРОНСКА АДРЕСА: ", validators=[DataRequired(), Email()])
    gender = SelectField("ПОЛ: ", choices=["", "машки", "женски"], validators=[DataRequired()])
    birth_date = DateField("ДАТУМ НА РАЃАЊЕ: ")
    register_btn= SubmitField("РЕГИСТРИРАЈ СЕ")

    def validate_email(self, field):
        try:
            user = Users.objects(email=field.data).get_or_404()
            raise ValidationError('Електронската адреса веќе постои.')
        except:
            pass


    def validate_username(self, field):
        try:
            user = Users.objects(username=field.data).get_or_404()
            raise ValidationError('Корисничкот име е веќе зафатено.')
        except:
            pass


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('СТАРА ЛОЗИНКА', validators=[DataRequired()])
    new_password = PasswordField('НОВА ЛОЗИНКА', validators=[
        DataRequired(), EqualTo('confirm_new_password', message='Лозинките мора да се совпаѓаат.')])
    confirm_new_password = PasswordField('ПОТВРДИ НОВА ЛОЗИНКА',
                              validators=[DataRequired()])
    submit_new_password = SubmitField('ЗАЧУВАЈ НОВА ЛОЗИНКА')


class PasswordResetRequestForm(FlaskForm):
    email_reset_password = StringField('ЕЛЕКТРОНСКА АДРЕСА', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit_reset_email = SubmitField('ИСПРАТИ ЛИНК ЗА ПРОМЕНА НА ЛОЗИНКА')


class PasswordResetForm(FlaskForm):
    password_reset = PasswordField('НОВА ЛОЗИНКА', validators=[
        DataRequired(), EqualTo('confirm_password_reset', message='Лозинките мора да се совпаѓаат.')])
    confirm_password_reset = PasswordField('ПОТВРДИ НОВА ЛОЗИНКА', validators=[DataRequired()])
    submit_reset_pass = SubmitField('ПРОМЕНИ ЛОЗИНКА')