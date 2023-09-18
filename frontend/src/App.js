import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [webcamImage, setWebcamImage] = useState('');
  const [vehicleDetection, setVehicleDetection] = useState('');
  const [licensePlateDetection, setLicensePlateDetection] = useState('');
  const [characterRecognition, setCharacterRecognition] = useState('');

  useEffect(() => {
    // Create a WebSocket connection
    const ws = new WebSocket('ws://localhost:5000/ws');

    // Set up event listeners for incoming WebSocket messages
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'webcam_image':
          setWebcamImage(data.data);
          break;
        case 'vehicle_detection':
          setVehicleDetection(data.data);
          break;
        case 'license_plate_detection':
          setLicensePlateDetection(data.data);
          break;
        case 'character_recognition':
          setCharacterRecognition(data.data);
          break;
        default:
          break;
      }
    };

    // Close the WebSocket connection when the component unmounts
    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="App">
      <div className="outlined-box">
        <h3>Webcam Image</h3>
        <p>{webcamImage}</p>
      </div>
      <div className="outlined-box">
        <h3>Vehicle Detection</h3>
        <p>{vehicleDetection}</p>
      </div>
      <div className="outlined-box">
        <h3>License Plate Detection</h3>
        <p>{licensePlateDetection}</p>
      </div>
      <div className="outlined-box">
        <h3>Character Recognition</h3>
        <p>{characterRecognition}</p>
      </div>
    </div>
  );
}

export default App;
