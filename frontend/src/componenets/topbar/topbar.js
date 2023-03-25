import React, { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext';
import './topbar.css'

export default function TopBar(props) { 
    let { currentUser } = useAuth()
    const [status, setStatus] = useState('admin')
  
    if(status == 'admin') {
      return(
        <div className='topbar-container'>
          <NavLink to='/' className='home-link'>Home</NavLink>
          <NavLink to='/user' className='user-link'>User</NavLink>
          <NavLink to='/game-settings' className='user-link'>Game Settings</NavLink>
          <NavLink to='/all-players' className='user-link'>Players</NavLink>
        <Link to='https://discord.gg/eHUqHnM' target='_blank' className='discord-link'>Discord</Link>
    </div>
      )
    } else

  return (
    <div className='topbar-container'>
        <NavLink to='/' className='home-link'>Home</NavLink>
        {!currentUser ? <NavLink to='/sign-in' className='sign-in-link' >Sign-In</NavLink> : <NavLink to='/user' className='user-link'>User</NavLink>}
        <Link to='https://discord.gg/eHUqHnM' target='_blank' className='discord-link'>Discord</Link>
    </div>
  )
}
