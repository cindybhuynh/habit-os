// habitos-frontend/src/LoginPage.jsx

import { useState } from 'react'
import './App.css'
import Wave from 'react-wavify'

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
    <div className='login-page-wrapper'>
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
      <Wave
      //  fill='#15A0D8'
       paused={false}
       options={{height: 45, amplitude: 20, speed: 0.13, points: 3 }}
       style={{
        position: 'absolute',
        bottom: -7,
        left: 0,
        right: 0,
        display: 'block',
        opacity: 0.8,
        marginBottom: 0,
       }}
       mask="url(#mask)" 
       fill="#15A0D8">
        <defs>
          <linearGradient id="gradient" gradientTransform="rotate(90)">
            <stop offset="0" stopColor="white" />
            <stop offset="1" stopColor="black" />
          </linearGradient>
          <mask id="mask">
            <rect x="0" y="0" width="2000" height="200" fill="url(#gradient)"  />
          </mask>
        </defs>
      </Wave>
    </div>
  )
}

export default LoginPage