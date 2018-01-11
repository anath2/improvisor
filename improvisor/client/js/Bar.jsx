import React from 'react'

const Bar = ({height, intensity}) => {

    let barStyle = {
        width: '56px',
        height: '56px',
        backgroundColor: '#E4F1FE',
        borderRadius: '16px'
    }

    return (
        <div className='bar' style={barStyle} />
    )
}

export default Bar