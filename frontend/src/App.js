import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const App = () => {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    // Connect to the WebSocket server when the component mounts
    const socket = io('http://localhost:5000'); // Replace with your server URL and port

    // Subscribe to the channel where image data will be sent
    socket.emit('subscribe', 'imageChannel'); // Use the correct channel name

    // Listen for incoming image data
    socket.on('uploaded_image', (data) => {
      // Handle the received image data here
      if (data.imageData) {
        setImageData(data.imageData);
      }
    });

    // Clean up the WebSocket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []); // Only run once when the component mounts

  return (
    <div>
      {imageData ? (
        <img src={`data:image/jpeg;base64,${imageData}`} alt="Vehicle" />
      ) : (
        <p>No image data received yet.</p>
      )}
    </div>
  );
};

export default App;
