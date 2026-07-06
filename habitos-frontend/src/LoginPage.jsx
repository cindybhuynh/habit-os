// habitos-frontend/src/LoginPage.jsx

import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL

function LoginPage({onLogin, onSwitchToRegister}) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        body: formData,
      })
      if (response.status === 200) {
        const data = await response.json()
        const token = data.access_token
        onLogin(token)
      }
      else {
        setError('Invalid credentials')
      }


    } catch (error) {
      setError('Could not connect to server')
        console.log('Error connecting to backend:', error)
    }
  }
  
  return (
    <div className="login-container">
      <h1>HabitOS</h1>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Log In</button>
        <p className="switch-to-register-button" onClick={onSwitchToRegister}>
          Don't have an account? Sign up
        </p>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  )
}

export default LoginPage