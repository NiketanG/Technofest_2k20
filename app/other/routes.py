from flask import render_template, Blueprint
from flask import current_app as app
from app import cache
other = Blueprint('other', __name__)

@other.route('/')
@cache.cached(timeout=6000)
def index():
    return render_template('/index.html', title='Welcome')

@other.route('/events')
@other.route('/events/')
@cache.cached(timeout=6000)
def events():
    return render_template('/Events.HTML', title='Events')

@other.route('/aboutus')
@other.route('/aboutus/')
@cache.cached(timeout=6000)
def aboutus():
    return render_template('/AboutUs.html', title='About Us')

@other.route('/contactus')
@other.route('/contactus/')
@cache.cached(timeout=6000)
def contactus():
    return render_template('/ContactUS.HTML', title='Contact Us')


