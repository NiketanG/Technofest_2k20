from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(e):
    return render_template("404.html")