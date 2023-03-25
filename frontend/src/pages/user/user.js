import React, { useEffect, useState } from 'react'
import { Button } from 'react-bootstrap'
import { Link, Navigate } from 'react-router-dom'
import { getUser } from '../../API/getUser'
import { useAuth } from '../../contexts/AuthContext'
import './user.css'

export default function User() {
    let { logout, currentUser } = useAuth()
    const [data, setData] = useState([])
    const [status, setStatus] = useState('Zombie')

    useEffect(() => {
      async function apiCall() {
        fetch(`http://localhost:5000/getSingleUserData/${currentUser.uid}`)
      .then((response) => response.json())
      .then((res) => setData(res.userData[1]))
      .catch(err => console.log(err));
      }
      console.log()
      apiCall()
    }, [])

    async function handleSubmit(e) {
    e.preventDefault()

    try {
        await logout()
    } catch(e) {
        console.log(e)
    }
    Navigate('/')
  }

  return (
    <div className='user-background'>
        <h1>You</h1>
        <h2>{data[4] + " " + data[5]}</h2>
        <h3>{data[0]}<Link to={`/tag/${currentUser.uid}`}>Got Tagged?</Link></h3>
        <h3>{data[11]}</h3>
        <Button className='buttonStyle w-100' onClick={handleSubmit}>Logout</Button>
    </div>
  )
}
