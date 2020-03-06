# Project 2

A chatroom flask app emulating Slack. Users can create and join channels and send and receive messages in real time. SocketIO used to broadcast messages and channels to all users. Adds an emoji selector from a javascript library. Doesn't work on mobile because of click event handling.

## Description of Files in repository

- application .py

	- handles socketio events, handles sessions and sign-in, defines message class, stores channels and messages as local variables. 

### Static

- lib
	- emoji library code from [emoji-picker](https://github.com/OneSignal/emoji-picker)

- chatroom.js
	- all the javascript for the chatroom. Broadcasting new messages and channels, toggling between channels, storing last visited channel in local storage. 

### Templates

- chatroom.html
	- main page for the chatroom
- landing.html
	- sign in page
- layout.html
	- template for other pages to inherit


