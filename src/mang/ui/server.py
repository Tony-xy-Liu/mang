import os
from pathlib import Path
from flask import Flask, request
from flask_socketio import SocketIO, emit
from constants import BIND

HERE = '/'.join(os.path.abspath(__file__).split('/')[:-1])
STATIC = Path("./mang-ui/build")
app = Flask(__name__, static_folder=STATIC)

bind_ip = BIND.replace("localhost", "127.0.0.1")
sio = SocketIO(
    app,
    cors_allowed_origins=[ # for some reason, the bind needs to be added to CORS
        f"http://{bind_ip}",
        f"https://{bind_ip}",
    ],
) 

#-----------------------------------------------------------------------------
# 

def getSecret():
    secret_path = f'{HERE}/secrets'
    os.system(f'mkdir -p {secret_path}')
    secret_path += '/secret'
    try:
        with open(secret_path, 'r') as s:
            return s.readlines()[0][:-1]
    except FileNotFoundError:
        import secrets
        with open(secret_path, 'w') as s:
            tok = secrets.token_urlsafe(64)
            s.write(tok)
            s.flush()
            return tok
app.config['SECRET_KEY'] = getSecret()

#-----------------------------------------------------------------------------
# REST

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    if path == "":
        return app.send_static_file('index.html')
    file_path = HERE/STATIC/Path(path)
    if file_path.exists():
        return app.send_static_file(path)
    return f"[{path}] not found", 404

#-----------------------------------------------------------------------------
# socketio

def get_sid(req):
    return req.sid

connected_users = {}

@sio.on('join')
def handle_join(data):
    username = data.get("username")
    if username is None: return False
    sid = get_sid(request)
    print(f'[{username}] joined as [{sid}]')
    connected_users[sid] = username
    emit('user_count', {'count': len(connected_users)}, broadcast=True)
    data = {
        'username': username, 
    }
    emit('user_joined', data, broadcast=True)

@sio.on('disconnect')
def handle_disconnect():
    username = connected_users[get_sid(request)]
    if username is None: return False
    print(f'[{username}] disconnected')
    del connected_users[get_sid(request)]
    emit('user_count', {'count': len(connected_users)}, broadcast=True)
    data = {
        'username': username, 
    }
    emit('user_left', data, broadcast=True)

@sio.on('send_message')
def handle_message(data):
    print(data)
    message = {
        'sender': data.get('sender', 'Anonymous'),
        'text': data['text'],
        'time': data.get('time', 'Now')
    }
    emit('new_message', message, broadcast=True)
