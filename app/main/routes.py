from flask import session, redirect, url_for, render_template, request

# from . import main
from app.main import bp

#from .forms import LoginForm
from app.main.forms import LoginForm


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form, title="Log In", name="", room="")


@bp.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    title= "Channel " + room
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', title=title, name=name, room=room)