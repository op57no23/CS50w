import os
from collections import deque
import pdb
from flask import Flask, session, render_template, request, url_for, redirect, flash, Markup
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {}
usernames = {}

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('chatroom'))
    else:
        return render_template('landing.html')

@app.route("/chatroom", methods = ["GET", "POST"])
def chatroom():
    if (request.method == "POST"):
        if request.form.get("username") in usernames:
            flash("This username is already in use. Please select another")
            return redirect(url_for('index'))
        username = request.form.get("username")
        session['username'] = username
        usernames[username] = True
    else:
        username = session['username']
    return render_template('chatroom.html', username = username, channels = channels)

@socketio.on("create_new_channel")
def create_channel(data):
    if data['channel_name'] not in channels:
        channels[data['channel_name']] = deque(maxlen=100) 
        emit("new channel", data, broadcast = True)

@socketio.on("create_new_message")
def create_message(data):
    channel_name = data['channel_name']
    time = data['time']
    message = Markup(data['message'])
    user = session['username']
    channels[channel_name].append(Message(user, message, time))
    emit("new message", {"time": time, "user": user, "message": message, "channel_name": channel_name}, broadcast = True)

class Message:

    def __init__(self, user, message, time):
        self.user = user
        self.message = message
        self.time = time

