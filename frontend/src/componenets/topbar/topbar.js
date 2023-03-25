import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import './topbar.css'

export default function TopBar(props) {
  return (
    <div className='topbar-container'>
        <NavLink to='/' className='home-link'>Home</NavLink>
        <NavLink to='/sign-in' className='sign-in-link' >Sign-In</NavLink>
        <Link to='/discord' className='discord-link'>Discord</Link>
    </div>
  )
}
