import { useState } from 'react'
import './App.css'
import SpeechRecognitionComponent from './audio'
// import AudioRecorder from './audio'


function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      {/* <AudioRecorder /> */}
      <SpeechRecognitionComponent />
    </div>
  )
}

export default App
