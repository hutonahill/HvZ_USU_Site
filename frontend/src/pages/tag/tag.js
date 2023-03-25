import React from 'react'
import './tag.css'
import item from './mockData.json'
import { Button } from 'react-bootstrap'
import { useLocation } from 'react-router-dom';

export default function Tag() {
    const player_id = useLocation().pathname.slice(5);
    console.log(player_id)

    function handleSubmit(item) {
        //TODO Tag API
    }
  return (
    <div className='tag-background'>
        {item.map( (item) =>
            <div className="player-wrapper">
            <h2 className="player-text">{item.name}</h2>
            <h2>{item.student_id}</h2>
            <h2>{item.player_id}</h2>
            <h2>{item.status}</h2>
            <Button className='buttonStyle w-100' onClick={() => handleSubmit(item)}>Tag Player</Button>
        </div>
        )}
    </div>
  )
}
