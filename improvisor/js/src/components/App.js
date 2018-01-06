import React from 'react';
import '../App.css';

import Waveform from './SoundAnimation'

const App = () => {
  return (
    <div className="App">
    <header className="App-header">
      <h1 className="App-title">Improvisor</h1>
    </header>
    <Waveform />
  </div>
  )
}

export default App;
