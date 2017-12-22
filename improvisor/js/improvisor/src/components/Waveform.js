import React, { Components } from 'react'

// Bar component whose height is set by the wave
const WaveBar = ({style}) => {
    return (
        <div className='wave-bar' style={style} />
    )
}

const WaveForm = () => {
    return (
        <div className='waveform-wrapper'>
        </div>
    )
}

export default WaveForm
