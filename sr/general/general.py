from flask import Blueprint, render_template

gen = Blueprint('general', __name__, url_prefix='/', template_folder='templates/general')


@gen.route('/')
def index():
    return render_template("index.html")