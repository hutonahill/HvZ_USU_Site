import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext';
import './topbar.css'

export default function TopBar(props) { 
    let { currentUser } = useAuth()

  return (
    <div className='topbar-container'>
        <NavLink to='/' className='home-link'>Home</NavLink>
        {!currentUser ? <NavLink to='/sign-in' className='sign-in-link' >Sign-In</NavLink> : <NavLink to='/user' className='user-link'>User</NavLink>}
        <Link to='/discord' className='discord-link'>Discord</Link>
    </div>
  )
}
