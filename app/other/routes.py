from flask import render_template, Blueprint

other = Blueprint('other', __name__)

@other.route('/')
def index():
    return render_template('/index.html', title='Welcome')

@other.route('/events')
@other.route('/events/')
def events():
    return render_template('/Events.HTML', title='Events')

@other.route('/aboutus')
@other.route('/aboutus/')
def aboutus():
    return render_template('/AboutUs.html', title='About Us')

@other.route('/contactus')
@other.route('/contactus/')
def contactus():
    return render_template('/ContactUS.HTML', title='Contact Us')


