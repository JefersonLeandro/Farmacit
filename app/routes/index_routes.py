from flask import Blueprint, render_template
# from app import db

bp = Blueprint('inicio', __name__)

@bp.route('/')
def index():
    return render_template('index.html')    




