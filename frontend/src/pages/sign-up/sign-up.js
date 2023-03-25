import React, { useRef, useState } from 'react'
import { Form, Card, Button, Alert } from 'react-bootstrap'
import { Container } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios';
import {useAuth} from '../../contexts/AuthContext';
import './sign-up.css'

export default function SignUp() {
  const emailRef = useRef()
  const passwordRef = useRef()
  const { signup } = useAuth()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  //asyncronous submit function
  async function handleSubmit(e) {
    e.preventDefault()

    try {
      setError('')
      setLoading(true)
      //waits for promise of login 
      const username = await signup(emailRef.current.value, passwordRef.current.value)
      const uid = username.user._delegate.uid

      navigate('/user')
    } catch(e) {
      setError('Failed to sign up (Password must contain at least 6 characters)')
      console.log(e)
    }
    setLoading(false)
  }

  return (
    <div className='sign-in-container'>
    <Container className='d-flex align-items-center justify-content-center' style={{ minHeight: "100vh" }}>
      <div className="w-100" style={{ maxWidth: "400px" }}>
        <>
          <Card className="SignUp-Card">
            <Card.Body>
              <h2 className="text-center mb-4 text-white">Sign Up for an Account</h2>
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form onSubmit={handleSubmit}>
                <Form.Group id="email" className="mt-4">
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="email" ref={emailRef} required />
                </Form.Group>
                <Form.Group id="password" className="mt-1">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" ref={passwordRef} required />
                </Form.Group>
                <Button disabled={loading} className='buttonStyle w-100 mt-4' type="submit">Signup</Button>
              </Form>
            </Card.Body>
          </Card>
        </>
      </div>
    </Container>
    </div>
  )
}