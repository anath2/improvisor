import React from 'react'
import Bar from './bar'

const Visualization = () => {
    const visualizationStyle = {
        position: 'absolute',
        top: '0',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        justifyContent: 'space-around',
        alignItems: 'center',
        width: '800px',
        height: '100vh',
        margin: 'auto',
        maxWidth: '100vw'
    }

    return (
        <div className='wrapper' style={visualizationStyle}>
            <div className='note note-c'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-c#'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-d'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-d#'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-e'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-f'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-f#'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-g'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-g#'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-a'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-a#'>
                <Bar height={1} intensity={0} />
            </div>
            <div className='note note-b'>
                <Bar height={1} intensity={0} />
            </div>
        </div>
    )
}

export default Visualization
