from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required

from app.decorators import admin_required, permission_required
from .. import db
from ..models import User, Permission
from ..email import send_email
from . import main
from .forms import NameForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session['known'] = False
#             if current_app.config['ADMIN']:
#                 send_email(current_app.config['ADMIN'], 'New User',
#                            'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('.index'))
#
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False))

@main.route('/cup')
def shit_test():
    return render_template('cup.html');
