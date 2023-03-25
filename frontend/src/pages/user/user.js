import React, { useState } from 'react'
import { Button } from 'react-bootstrap'
import { Link, Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import './user.css'

export default function User() {
    let { logout } = useAuth()
    const [status, setStatus] = useState('Zombie')

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
        <h2>First Name</h2>
        <h3>Player ID <Link to={'/tag/'}>Got Tagged?</Link></h3>
        <h3>{status}</h3>
        <Button className='buttonStyle w-100' onClick={handleSubmit}>Logout</Button>
    </div>
  )
}
