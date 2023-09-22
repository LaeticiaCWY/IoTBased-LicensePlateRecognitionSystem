from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Maintain a dictionary to store uploaded images
uploaded_images = {}

@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data': 'This text was fetched using an HTTP call to the server on render'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when a client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when a client types a message"""
    print("data from the front end: ", str(data))
    emit("data", {'data': data, 'id': request.sid}, broadcast=True)

@socketio.on('upload_image')
def handle_image_upload(data):
    """event listener for image uploads from the LPR script"""
    image_data = data.get('imageData')
    if image_data:
        # Decode base64 image data
        decoded_image = base64.b64decode(image_data)
        
        # Store the image in the dictionary with a unique identifier (e.g., request.sid)
        uploaded_images[request.sid] = decoded_image
        
        emit("image_uploaded", {"message": "Image uploaded successfully"}, room=request.sid)

@socketio.on("get_uploaded_image")
def get_uploaded_image(data):
    """event listener to retrieve uploaded images"""
    session_id = data.get('sessionId')
    image = uploaded_images.get(session_id)
    if image:
        # Send the image data to the requesting client
        emit("uploaded_image", {"imageData": base64.b64encode(image).decode('utf-8')}, room=session_id)

@socketio.on("disconnect")
def disconnected():
    """event listener when a client disconnects from the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
