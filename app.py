from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from app.controller.agent import create_agent

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', async_handlers=True)

# Create agent with socketio instance
agent = create_agent(socketio)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET', 'POST'])
def test():
    return jsonify({'message': 'Hello World!'})

def stream_agent_response(input_text):
    try:
        # The agent will now handle streaming through callbacks
        response = agent.invoke(
            {"input": input_text}
        )
    except Exception as e:
        socketio.emit('agent_update', {
            'type': 'error',
            'data': {
                'error': str(e)
            }
        })

@socketio.on('user_input')
def handle_user_input(data):
    """Handle incoming WebSocket messages"""
    if isinstance(data, dict) and 'input' in data:
        stream_agent_response(data['input'])
    else:
        socketio.emit('agent_update', {
            'type': 'error',
            'data': {
                'error': 'Invalid input format'
            }
        })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=9000)