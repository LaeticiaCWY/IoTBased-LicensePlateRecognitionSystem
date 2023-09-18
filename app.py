import asyncio
import json
import websockets
from flask import Flask

app = Flask(__name__)

# Store connected clients in a set
connected_clients = set()

@app.route('/')
def index():
    return "WebSocket server is running"

# Define a WebSocket route
@app.websocket('/ws')
async def ws_handler(ws):
    # Add the client to the set of connected clients
    connected_clients.add(ws)

    try:
        async for message in ws:
            # Handle WebSocket messages if needed
            pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Remove the client from the set when the connection is closed
        connected_clients.remove(ws)

async def send_updates():
    while True:
        # Simulate receiving results from your LPR script
        webcam_image = "webcam_image_data"
        vehicle_detection = "vehicle_detection_data"
        license_plate_detection = "license_plate_detection_data"
        character_recognition = "character_recognition_data"

        # Send data to all connected clients
        for client in connected_clients:
            await client.send(json.dumps({"type": "webcam_image", "data": webcam_image}))
            await client.send(json.dumps({"type": "vehicle_detection", "data": vehicle_detection}))
            await client.send(json.dumps({"type": "license_plate_detection", "data": license_plate_detection}))
            await client.send(json.dumps({"type": "character_recognition", "data": character_recognition}))

        await asyncio.sleep(5)  # Simulate a delay between sending updates

if __name__ == '__main__':
    # Create an asyncio event loop
    loop = asyncio.get_event_loop()
    
    # Start the send_updates coroutine in the event loop
    asyncio.ensure_future(send_updates())

    # Start the Flask app
    app.run()
