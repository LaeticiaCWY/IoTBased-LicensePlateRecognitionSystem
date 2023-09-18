import json
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Store connected clients in a set
connected_clients = set()

@app.route('/')
def index():
    return "WebSocket server is running"

# Define a WebSocket route using Flask-SocketIO
@socketio.on('connect')
def handle_connect():
    connected_clients.add(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    connected_clients.remove(request.sid)

@socketio.on('message')
def handle_message(message):
    # Handle WebSocket messages if needed
    pass

def send_updates():
    while True:
        # Simulate receiving results from your LPR script
        webcam_image = "webcam_image_data"
        vehicle_detection = "vehicle_detection_data"
        license_plate_detection = "license_plate_detection_data"
        character_recognition = "character_recognition_data"

        # Send data to all connected clients
        for client in connected_clients:
            socketio.emit('webcam_image', {"data": webcam_image}, room=client)
            socketio.emit('vehicle_detection', {"data": vehicle_detection}, room=client)
            socketio.emit('license_plate_detection', {"data": license_plate_detection}, room=client)
            socketio.emit('character_recognition', {"data": character_recognition}, room=client)

        socketio.sleep(5)  # Simulate a delay between sending updates

if __name__ == '__main__':
    # Start the Flask-SocketIO app
    socketio.start_background_task(send_updates)
    socketio.run(app, debug=True)
