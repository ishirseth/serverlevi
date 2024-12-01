from flask import Flask
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game state
class GameState:
    def __init__(self):
        self.players = {}
        self.coin = {'x': 400, 'y': 300}

game_state = GameState()

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('player_id', {'id': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    if request.sid in game_state.players:
        del game_state.players[request.sid]
    emit('game_state', game_state.players, broadcast=True)

@socketio.on('player_update')
def handle_player_update(data):
    game_state.players[request.sid] = data
    emit('game_state', game_state.players, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) 