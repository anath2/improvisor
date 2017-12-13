import React from 'react';
import '../App.css';

import Waveform from './Waveform'

const App = () => {
  return (
    <div className="App">
    <header className="App-header">
      <h1 className="App-title">Improvisor</h1>
      <Waveform />
    </header>
  </div>
  )
}

export default App;
