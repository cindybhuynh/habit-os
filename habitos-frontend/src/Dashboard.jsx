import { useState, useEffect } from 'react'
import './App.css'

function Dashboard() {
    const [habits, setHabits] = useState([])
    const [habitName, setHabitName] = useState('')
    const [scheduleType, setScheduleType] = useState('daily')
    const [targetCount, setTargetCount] = useState('')
    const [startDate, setStartDate] = useState('')
    const [notes, setNotes] = useState('')
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
    const handleCreateHabit = async () => {
        try {
            const response = await fetch('http://localhost:8000/habits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: habitName,
                schedule_type: scheduleType,
                target_count: parseInt(targetCount),
                start_date: startDate,
                notes: notes || null,
            }),
            })
            const newHabit = await response.json()
            setHabits([...habits, newHabit])
            setHabitName('')
            setTargetCount('')
            setStartDate('')
            setNotes('')
        } catch (error) {
            console.log('Error creating habit:', error)
        }
    }
    const toggleHabit = async (habitId) => {
        const today = new Date().toISOString().split('T')[0];
        const res = await fetch(
            `http://localhost:8000/habits/${habitId}/completions/toggle/${today}`,
            { method: 'POST' }
        );
        const data = await res.json();
        // Update the habit's completed status in your state
        setHabits(prev => prev.map(h => 
            h.id === habitId ? { ...h, completed: data.completed } : h
        ));
    };
    return(
        <div className='dashboard'>
            <h1>Dashboard</h1>
            <p>You are logged in!</p>

            <div className='create-habit-form'>
                <h2>Create a New Habit</h2>
                <input 
                    type="text"
                    placeholder="Habit Name"
                    value={habitName}
                    onChange={(e) => setHabitName(e.target.value)}
                />
                <select value={scheduleType} onChange={(e) => setScheduleType(e.target.value)}>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                </select>
                <input 
                    type="number"
                    placeholder="Target count"
                    value={targetCount}
                    onChange={(e) => setTargetCount(e.target.value)}
                />
                <input 
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Notes (Optional)"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
                <button onClick={handleCreateHabit}>Add Habit</button>
            </div>
            {habits.map((habit) => (
                <div key={habit.id} className="habit-card">
                    <input 
                        type="checkbox" 
                        checked={habit.completed || false} 
                        onChange={() => toggleHabit(habit.id)} 
                    />
                    <h2>{habit.name}</h2>
                    <p>{habit.schedule_type} · Target: {habit.target_count}</p>
                    {habit.notes && <p>{habit.notes}</p>}
                </div>
            ))}
        </div>
    )
}

export default Dashboard