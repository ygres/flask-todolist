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
from .models import Tasks, db
from .forms import TasksCreateForm, TasksUpdateForm
from flask_wtf.csrf import CSRFProtect
from app.utils.db import sqlalchemy_orm_to_dict
from flask_login import current_user, login_required

module = Blueprint('tasks', __name__)
csrf = CSRFProtect()

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/', methods=['GET'])
@module.route('/page/<int:page>/', methods=['GET'])
def index(page=1):
    tasks = None
    try:
        tasks = Tasks.query.paginate(page=page, per_page=5, error_out=True)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return render_template('tasks/index.html', object_list=tasks)


@module.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TasksCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            tasks = Tasks(**form.data)
            tasks.user_id = current_user.id
            db.session.add(tasks)
            db.session.flush()
            # id = tasks.id
            db.session.commit()
            flash("The task was successfully added!", "success")
            return redirect(url_for('tasks.index'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('There was error while querying database', 'error')
    return render_template('tasks/create.html', form=form)

@module.route('/task/remove/<int:id>', methods=['GET'])
@login_required
def remove_task(id):
    tasks = None
    try:
        tasks = Tasks.query.filter_by(id=id).first_or_404()
        db.session.delete(tasks)
        db.session.commit()
        flash('Task was successful removed!', 'success')

        return redirect(url_for('tasks.index'))
    #entity = Tasks.query.get_or_404(id)
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error('Uncaught exception while querying database at tasks.remove', exc_info=e)
        flash('Uncaught exception while querying database', 'danger')
        abort(500)
    return render_template('tasks/index.html')

@module.route('/task/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    form = TasksUpdateForm(request.form)
    task = Tasks.query.get_or_404(id)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            for key, val in form.data.items():
                if hasattr(task, key):
                    setattr(task, key, val)
            db.session.commit()
            flash('Task successful updated!', 'success')
            return redirect(url_for('tasks.index'))
        else:
            form = TasksUpdateForm(**sqlalchemy_orm_to_dict(task))
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error('Uncaught exception while querying database at entity.update', exc_info=e)
        flash('Uncaught error while querying database', 'danger')
        abort(500)
    return render_template('tasks/update.html', form=form, id=id)
