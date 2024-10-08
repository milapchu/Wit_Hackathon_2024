from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from website import db


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/group')
@login_required
def group():
    return render_template("group.html", user=current_user)

