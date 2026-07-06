// habitos-frontend/src/RegisterPage.jsx

import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL

function RegisterPage({onRegister, onSwitchToLogin}) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
        const registerResponse = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        })

        if (registerResponse.status === 201) {
            const loginFormData = new URLSearchParams()
            loginFormData.append('username', email)
            loginFormData.append('password', password)

            const loginResponse = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                body: loginFormData,
            })
            
            if (loginResponse.status === 200) {
                const data = await loginResponse.json()
                onRegister(data.access_token)
            }
            else {
                setError('Registered successfully but auto login failed. Please log in.')
            }
        }
        else if (registerResponse.status === 409) {
            setError('An account with this email already exists')
        }
        else if (registerResponse.status === 422) {
            setError('Please check your email format and use a password with at least 8 characters')
        }
        else {
            setError('Registration failed')
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
        <button type="submit">Register</button>
        <p className="switch-to-login-button" onClick={onSwitchToLogin}>
            Already have an account? Log in
        </p>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  )
}

export default RegisterPage