import React, { useState } from 'react'
import { Button } from 'react-bootstrap'
import { Navigate } from 'react-router-dom'
import './game-settings.css'

export default function GameSettings() {
    const [status, setStatus] = useState("admin")

    const handlePause = () => {
        //TODO
    }
    const handleReset = () => {
        //TODO
    }
    if (status == "admin") { return(
    <div className='game-settings-background'>
        <div className='pause-game'>  
            <h4>Pauses all gameplay not allowing any human to be tagged</h4>
            <Button>Pause Game</Button>
        </div>
        <div className='reset-game'>
            <h4>Resets all Players to humans</h4>           
            <Button>Reset Game</Button>
        </div>
    </div>
    )} else return (
        <Navigate to={'/'}/>
    )
}
