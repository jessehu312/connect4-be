from flask import request, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from datetime import datetime
from app.services.radar import radar_client
from threading import Timer

STALE_CLIENT_THRESHOLD = 30 # seconds
blueprint = Blueprint('update', __name__, url_prefix='/update')

def init_socketio(app):
  socketio = SocketIO()
  socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins='*')
  register_handlers(socketio)
  return socketio

def register_handlers(socketio):
  lobby = {}
  match = {}

  @socketio.on('connect')
  def handle_connect():
    pass

  @socketio.on('register')
  def handle_register(data):
    lobby[data['id']] = data
    join_room('lobby')
    emit('lobby', lobby, room='lobby')

  @socketio.on('disconnect')
  def handle_disconnect():
    if request.sid in lobby:
      lobby.pop(request.sid)
    leave_room('lobby')
    emit('lobby', lobby, room='lobby')

  @socketio.on('challenge')
  def handle_challenge(id):
    print(f'{id} challenged')
    emit('challenged', request.sid, room=id)

  @socketio.on('accept')
  def handle_accept(data):
    matchid = data['id']
    players = data['players']
    id = players[1] if players[0] == request.sid else players[0]
    if not id in lobby or not request.sid in lobby:
      emit('lobby', lobby, room='lobby')
      return
    lobby.pop(id)
    lobby.pop(request.sid)
    leave_room('lobby',id)
    leave_room('lobby',request.sid)
    emit('lobby', lobby, room='lobby')
    emit('accept', data, room=id)

  @socketio.on('match')
  def send_board(data):
    if data['id'] not in match:
      match[data['id']] = data['players']
    p1, p2 = match[data['id']]
    if request.sid == p1:
      emit('match', data['board'], room=p2)
    else:
      emit('match', data['board'], room=p1)
