import React, { useEffect, useState } from 'react'
import { Button } from 'react-bootstrap';
import { Navigate, useNavigate } from 'react-router-dom';
import './all-players.css'

export default function AllPlayers() {
    const [data, setData] = useState([])
    const [searchInput, setSearchInput] = useState("");
    const [inputText, setInputText] = useState("");
    const [filterRole, setFilterRole] = useState("");
    const [status, setStatus] = useState("admin")

    let navigate = useNavigate()

    function handleSubmit(item) {
        navigate(`/tag/${item[1]}`)
    }

    useEffect(() => {
      async function apiCall() {
        fetch(`http://localhost:5000/getAllUserData`)
      .then((response) => response.json())
      .then((res) => setData(res.userData))
      .catch(err => console.log(err));
      }
      console.log()
      apiCall()
    }, [])

    let inputHandler = (e) => {
      //convert input text to lower case
      var lowerCase = e.target.value.toLowerCase();
      setInputText(lowerCase);
      setSearchInput(e.target.value);
    };

    //create a new array by filtering the original array
    let filteredData = data.filter((el) => {
        if (inputText !== "") {
            return el[4].toLowerCase().includes(inputText)
        } else {
            return el
        }
    })
    if (status == "admin") { return(
    <div className='all-players-background'>
        <input className="search" type="text" placeholder="Search for a Player" onChange={inputHandler} value={searchInput}/>
        <div className="list">
            <div className="player-list">
                {filteredData.slice(1).map((item) => (
                    <div className="player-wrapper">
                        <h2 className="player-text">{item[4] + ' ' + item[5]}</h2>
                        <h2>{item[2]}</h2>
                        <h2>{item[0]}</h2>
                        <h2>{item[7]}</h2>
                        <Button className='buttonStyle w-100' onClick={() => handleSubmit(item)}>Tag Player</Button>
                    </div>
                ))}
        </div>
    </div>
    </div>)
    } else {
        return (
            <Navigate to={'/'}/>
        )
    }
}
