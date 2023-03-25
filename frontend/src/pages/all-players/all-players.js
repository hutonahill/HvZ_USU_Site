import React, { useState } from 'react'
import { Button } from 'react-bootstrap';
import { Navigate, useNavigate } from 'react-router-dom';
import './all-players.css'
import data from './mockData.json'

export default function AllPlayers() {
    const [searchInput, setSearchInput] = useState("");
    const [inputText, setInputText] = useState("");
    const [filterRole, setFilterRole] = useState("");
    let navigate = useNavigate()

    function handleSubmit(item) {
        navigate(`/tag/${item.player_id}`)
    }

    let inputHandler = (e) => {
      //convert input text to lower case
      var lowerCase = e.target.value.toLowerCase();
      setInputText(lowerCase);
      setSearchInput(e.target.value);
    };

    //create a new array by filtering the original array
    let filteredData = data.filter((el) => {
        if (inputText !== "") {
            return el.name.toLowerCase().includes(inputText)
        } else {
            return el
        }
    })
  return (
    <div className='all-players-background'>
        <input className="search" type="text" placeholder="Search for a Hero" onChange={inputHandler} value={searchInput}/>
        <div className="list">
            <div className="player-list">
                {filteredData.map((item) => (
                    <div className="player-wrapper">
                        <h2 className="player-text">{item.name}</h2>
                        <h2>{item.student_id}</h2>
                        <h2>{item.player_id}</h2>
                        <h2>{item.status}</h2>
                        <Button className='buttonStyle w-100' onClick={() => handleSubmit(item)}>Tag Player</Button>
                    </div>
                ))}
        </div>
    </div>
    </div>
  )
}
