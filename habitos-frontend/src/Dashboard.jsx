import { useState, useEffect } from 'react'
import './App.css'

function Dashboard() {
    const [habits, setHabits] = useState([])
    useEffect(() => {
        const fetchHabits = async () => {
            try {
            const response = await fetch('http://localhost:8000/habits')
            const data = await response.json()
            setHabits(data)
            } catch (error) {
            console.log('Error fetching habits:', error)
            }
        }
        fetchHabits()
    }, [])
    return(
        <div className='dashboard'>
            <h1>Dashboard</h1>
            <p>You are logged in!</p>
            {habits.map((habit) => (
                <div key={habit.id} className="habit-card">
                    <h2>{habit.name}</h2>
                    <p>{habit.schedule_type} · Target: {habit.target_count}</p>
                    <p>{habit.notes}</p>
                </div>
            ))}
        </div>
    )
}

export default Dashboard