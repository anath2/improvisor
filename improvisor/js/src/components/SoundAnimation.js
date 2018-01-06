/*
 *  The visualization contains 12 bars each representing
 * 12 notes of the chromatic scale. The height and color
 * of the notes represent the volume or amplitude of the
 * notes
 */

import React, { Components } from 'react'

// Bar component whose height is set by the wave
const NoteBar = ({style}) => {
    return (
        <div className='note-bar' style={style} />
    )
}

const SoundAnimation = ({soundData}) => {
    return (
        <div className='wrapper'>
            <div className='animation-title'>
                Who's playing goes here
            </div>
            <div className='notes-wrapper'>
                <NoteBar className='note-c note'  style={{'height': '30px'}}  />
                <NoteBar className='note-c# note' style={{'height': '30px'}}  />
                <NoteBar className='note-d note'  style={{'height': '30px'}}  />
                <NoteBar className='node-d# note' style={{'height': '30px'}}  />
                <NoteBar className='node-e note'  style={{'height': '30px'}}  />
                <NoteBar className='note-f note'  style={{'height': '30px'}}  />
                <NoteBar className='note-f# note' style={{'height': '30px'}}  />
                <NoteBar className='note-g note'  style={{'height': '30px'}}  />
                <NoteBar className='node-g# note' style={{'height': '30px'}}  />
                <NoteBar className='node-a note'  style={{'height': '30px'}}  />
                <NoteBar className='node-a# note' style={{'height': '30px'}}  />
                <NoteBar className='node-b note'  style={{'height': '30px'}}  />
            </div>
            <div className='animation-axis'>
                <div className='note-label'>C</div>
                <div className='note-label'>D</div>
                <div className='note-label'>E</div>
                <div className='note-label'>F</div>
                <div className='note-label'>G</div>
                <div className='note-label'>A</div>
                <div className='note-label'>B</div>
            </div>
        </div>
    )
}

export default SoundAnimation
