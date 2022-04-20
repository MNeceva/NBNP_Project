from flask import render_template, redirect, request, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import Users
from .forms import *
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        # current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/непотврден-профил')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.upload_files'))
    return render_template('auth/unconfirmed.html')


@auth.route('/најава', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.upload_files'))
    else:
        form = LoginForm(request.form)

        if form.validate_on_submit() and request.method == 'POST':
            try:
                user = Users.objects(email=form.email_login.data.lower()).get_or_404()

                if user.verify_password(form.password_login.data):
                    print(f"Remember me value: {form.remember_me.data}")
                    login_user(user, remember=form.remember_me.data)
                    next = request.args.get('next')
                    if next is None or not next.startswith('/'):
                        next = url_for('main.upload_files')
                    return redirect(next)
                # print("Invalid username or password")
                flash('Погрешна електронска адреса или лозинка!')
            except:
                flash("Не постои корисник со таква електронска адреса!")
                # raise AttributeError("This user doesn't exist!")
        
    return render_template('auth/login.html', form=form)


@auth.route('/одјава')
@login_required
def logout():
    logout_user()
    flash("Успешна одјава од кориснички профил!")
    return redirect(url_for('index'))


@auth.route('/регистрација', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.upload_files"))
    else:
        form = RegisterForm(request.form)

        if form.validate_on_submit() and request.method == "POST":
            user = Users(firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data.lower(),
            gender=form.gender.data,
            birthdate=(form.birth_date.data.strftime('%m/%d/%Y')))

            user.password = form.password.data
            
            user.save()
            user.reload()
            token = user.generate_confirmation_token()
            send_email(user.email, 'Активација на кориснички профил',
                    'auth/email/confirm', user=user, token=token)
            flash('На Вашата електронска адреса е испратена порака за активација на Вашиот кориснички профил!')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/потврди/<token>')
@login_required
def confirm(token):
    # print("I am in!\n")
    if current_user.confirmed:
        flash('Активацијата на корисничкиот профил е веќе направена. Продолжете кон најавување на истиот.')
        return redirect(url_for('auth.login'))

    if current_user.confirm(token):
        flash('Извршивте успешна активација на Вашиот кориснички профил!')
    else:
        flash('Линкот за активација на корисничкиот профил е невалиден или е со помината важност!')
    return redirect(url_for('main.upload_files'))


@auth.route('/потврди-повторно')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Активација на кориснички профил',
            'auth/email/confirm', user=current_user, token=token)
    flash('Проверете ја Вашата електронска пошта. Испратена е нова порака за активација на Вашиот профил.')
    return redirect(url_for('index'))


@auth.route('/промени-лозинка', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit() and request.method == "POST":
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            current_user.save()
            # current_user.update(password=form.password.data)
            flash('Вашата лозинка е успешно променета!')
            return redirect(url_for('main.upload_files'))
        else:
            flash('Погрешна тековна лозинка!')
    return render_template("auth/change_password.html", form=form)


@auth.route('/заборавена-лозинка', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        try:
            # print(len(Users.objects(email=form.email_reset_password.data).get_or_404()))
            user = Users.objects(email=form.email_reset_password.data).get_or_404()
            # print("Pominuvam 1")
            token = user.generate_reset_token()
            # print("Pominuvam 2")
            send_email(user.email, 'Променете ја Вашата лозинка',
                       'auth/email/reset_password',
                       user=user, token=token)
            # print("Pominuvam 3")
            flash('На Вашата електронска адреса е испратена порака со инструкции за промена на заборавената лозинка.')
            return redirect(url_for('auth.login'))
        except:
            # print('Непостоечка електронска адреса!')
            flash('Непостоечка електронска адреса!')
            
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/заборавена-лозинка/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm(request.form)
    if form.validate_on_submit() and request.method == "POST":
        print("I am in reset password")
        if Users.reset_password(token, form.password_reset.data):
            # db.session.commit()
            print("Reseting")
            flash('Вашата лозинка беше успешно променета!')
            return redirect(url_for('auth.login'))
        else:
            flash('Линкот за активација на корисничкиот профил е невалиден или е со помината важност!')
            return redirect(url_for('index'))
    return render_template('auth/reset_password.html', form=form)