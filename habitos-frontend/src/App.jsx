import { useState } from 'react'
import './App.css'
import LoginPage from './LoginPage.jsx'
import Dashboard from './Dashboard.jsx'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const handleLogin = () => {
    setIsLoggedIn(true)
  }
  return (
    <div>
      {isLoggedIn ? <Dashboard /> : <LoginPage onLogin={handleLogin} />}
    </div>
  )
}

export default App