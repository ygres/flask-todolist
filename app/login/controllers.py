from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect,
    request,
    url_for
)
from sqlalchemy.exc import SQLAlchemyError
from .models import Users, db
from .forms import LoginCreateForm, RegisterCreateForm
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required, login_user, current_user, logout_user

module = Blueprint('login', __name__)
csrf = CSRFProtect()

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/login', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    form = LoginCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            user = Users.query.filter_by(username=str(form.username.data).strip()).first()
            if user and user.check_password(str(form.password.data).strip()):
                login_user(user)
                redirect(url_for('tasks.index'))
            else:
                flash("Wrong login or password", "danger")
                return render_template('login/auth.html', form=form)

            return redirect(url_for('login.auth'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        flash('There was error while querying database', 'error')
    return render_template('login/auth.html', form=form)

@module.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('tasks.index'))

@module.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    form = RegisterCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            if str(request.form.get('password_confirm')).strip() != str(form.password.data).strip():
                flash("You entered different passwords, try again.", "danger")
                return render_template('login/register.html', form=form)
            user = Users(**form.data)
            user.set_password(str(form.password.data).strip())
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            login_user(user)
            flash("Congratulations, you have successfully registered", "success")
            return redirect(url_for('tasks.index'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
    return render_template('login/register.html', form=form)
