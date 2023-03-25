import React, { useEffect, useState } from 'react'
import './tag.css'
import item from './mockData.json'
import { Button } from 'react-bootstrap'
import { useLocation } from 'react-router-dom';

export default function Tag() {
    const player_id = useLocation().pathname.slice(5);
    const [data, setData] = useState([])
    console.log(player_id)

    useEffect(() => {
      async function apiCall() {
        fetch(`http://localhost:5000/getSingleUserData/${player_id}`)
      .then((response) => response.json())
      .then((res) => setData(res.userData[1]))
      .catch(err => console.log(err));
      }
      console.log()
      apiCall()
    }, [])

    function handleSubmit(item) {
        //TODO Tag API
    }
  return (
    <div className='tag-background'>
            <div className="player-wrapper">
            <h2 className="player-text">{data[4] + " " + data[5]}</h2>
            <h2>{data[2]}</h2>
            <h2>{data[0]}</h2>
            <h2>{data[11]}</h2>
            <Button className='buttonStyle w-100' onClick={() => handleSubmit(item)}>Tag Player</Button>
            </div>
    </div>
  )
}
