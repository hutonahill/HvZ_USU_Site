import React, { useRef, useState } from 'react'
import { Form, Card, Button, Alert } from 'react-bootstrap'
import { Container } from 'react-bootstrap'
import { useAuth } from '../../contexts/AuthContext'
import { Link } from'react-router-dom'
import './forgot-password.css'

export default function ForgotPassword() {
  const emailRef = useRef()
  const { resetPassword } = useAuth()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()

    try {
        setMessage('')
        setError('')
        setLoading(true)
        await resetPassword(emailRef.current.value)
        setMessage('Check your inbox for further instructions')
    } catch {
        setError('Failed to send email')
    }
    setLoading(false)
  }

  return (
    <div className='forgot-password-container'>
    <Container className='d-flex align-items-center justify-content-center' style={{ minHeight: "100vh" }}>
      <div className="w-100" style={{ maxWidth: "400px" }}>
        <>
          <Card className="SignUp-Card">
            <Card.Body>
              <h2 className="text-center mb-4 text-white">Password Reset</h2>
              {error && <Alert variant="danger">{error}</Alert>}
              {message && <Alert variant="success">{message}</Alert>}
              <Form onSubmit={handleSubmit}>
                <Form.Group id="email">
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="email" ref={emailRef} required />
                </Form.Group>
                <Button disabled={loading} className='buttonStyle w-100' type="submit">Reset Password</Button>
              </Form>
              <div className="w-100 text-center mt-3 text-white">
                <Link to="/sign-in">Login</Link>
              </div>
            </Card.Body>
          </Card>
          <div className="w-100 text-center mt-2 text-white">
            Need an account? <Link to='/sign-up'>Sign Up</Link>
          </div>
        </>
      </div>
    </Container>
    </div>
  )
}
