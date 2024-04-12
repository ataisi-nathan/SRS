import React, { useState } from 'react';
import socketIOClient from 'socket.io-client';

const SpeechRecognitionComponent = () => {
    const [transcription, setTranscription] = useState('');
    const [connect, setConnect] = useState(false)
    const [connectText, setConnectText] = useState('Connect')



    const handleSpeechRecognition = async () => {
        const socket = socketIOClient('http://localhost:5000');

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    socket.emit('audio-stream', event.data);
                }
            };

            mediaRecorder.start();

            // Stop recording after 5 seconds (adjust as needed)
            setTimeout(() => {
                mediaRecorder.stop();
                socket.disconnect();
            }, 5000);
        } catch (error) {
            console.error('Error capturing audio:', error);
        }
    };

    const connectToSocket = () => {
        const socket = socketIOClient('http://localhost:5000');
        if (!connect) {
            setConnectText('Disconnect')
            socket.on('message', (data) => { // Listen for data on the WebSocket connection
                setTranscription(data);
            });
        }else {
            setConnectText('Connect')
            socket.off();
        }
        setConnect(!connect)
    };

    return (
        <div className='container'>
            <button onClick={handleSpeechRecognition}>Click <br /> To <br /> Start</button>
            <button className='socket' onClick={connectToSocket}>{connectText}</button>
            <div>Transcription: {transcription}</div>
        </div>
    );
};

export default SpeechRecognitionComponent;
