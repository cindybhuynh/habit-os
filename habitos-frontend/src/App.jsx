// habitos-frontend/src/App.jsx

import { useState, useEffect } from 'react'
import './App.css'
import LoginPage from './LoginPage.jsx'
import Dashboard from './Dashboard.jsx'
import RegisterPage from './RegisterPage.jsx'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [view, setView] = useState('login')

  useEffect(() => {
        const token = localStorage.getItem('token')
        if (token) {
          setIsLoggedIn(true)
        }
    }, [])
  
  const handleLogin = (token) => {
    if (token) {
      localStorage.setItem("token", token)
      setIsLoggedIn(true)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    setIsLoggedIn(false)
  }
  
  return (
    <div>
      {isLoggedIn ? (
        <Dashboard onLogout={handleLogout}/>
      ) : view === 'login' ? (
        <LoginPage
          onLogin={handleLogin}
          onSwitchToRegister={() => setView('register')}
        />
      ) : (
        <RegisterPage
          onRegister={handleLogin}
          onSwitchToLogin={() => setView('login')}/>
      )}
    </div>
  )
}

export default App