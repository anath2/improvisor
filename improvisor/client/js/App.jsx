import React from 'react'
import Visualization from './Visualization'

const App = () => {

    let titleStyle = {
        fontFamily: 'Oswald, sans-serif',
        border: '1px solid #000',
        padding: '12px',
        display: 'inline-block',
        margin: '48px 0',
        textTransform: 'upperCase',
        letterSpacing: '1px'
    }
    return (
        <div className='wrapper' style={{textAlign: 'center'}}>
            <h2 className='text-center' style={titleStyle}>Improvisor</h2>
            <Visualization />
        </div>
    )
}

export default App
