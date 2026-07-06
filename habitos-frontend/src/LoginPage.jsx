import { useState } from 'react'
import './App.css'

function LoginPage({onLogin}) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const handleSubmit = async () => {
    try {
        const response = await fetch('http://localhost:8000/habits')
        const data = await response.json()
        console.log('Habits from backend:', data)
        onLogin()
    } catch (error) {
        console.log('Error connecting to backend:', error)
    }
  }
  return (
    <div className="login-container">
      <h1>HabitOS</h1>
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleSubmit}>Log In</button>
    </div>
  )
}

export default LoginPage