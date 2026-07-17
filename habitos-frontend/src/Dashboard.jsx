// habitos-frontend/src/Dashboard.jsx

import { useState, useEffect } from 'react'
import './App.css'
import apiFetch from './apiFetch'
import HabitHeatmap from './HabitHeatmap'
import DailyQuote from './DailyQuote'

const API_URL = import.meta.env.VITE_API_URL

function Dashboard({onLogout}) {
    const [habits, setHabits] = useState([])
    const [habitName, setHabitName] = useState('')
    const [scheduleType, setScheduleType] = useState('daily')
    const [targetCount, setTargetCount] = useState('')
    const [startDate, setStartDate] = useState('')
    const [notes, setNotes] = useState('')
    const [expandedHabitId, setExpandedHabitId] = useState(null)
    const [heatmapRefresh, setHeatmapRefresh] = useState(0)
    const [error, setError] = useState('')

    useEffect(() => {
        const fetchHabits = async () => {
            try {
            const response = await apiFetch(`${API_URL}/habits`)
            const data = await response.json()
            setHabits(data)
            } catch (error) {
            console.log('Error fetching habits:', error)
            }
        }
        fetchHabits()
    }, [])

    const handleCreateHabit = async () => {
        setError('')
        if (!habitName.trim() || !targetCount || !startDate) {
            setError('Please fill in habit name, target count, and start date')
            return
        }
        try {
            const response = await apiFetch(`${API_URL}/habits`, {
            method: 'POST',
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
        const res = await apiFetch(
            `${API_URL}/habits/${habitId}/completions/toggle/${today}`,
            { method: 'POST' }
        );
        const data = await res.json();

        setHabits(prev => prev.map(h => 
            h.id === habitId ? { ...h, completed_on_date: data.completed } : h
        ));
        
        setHeatmapRefresh(prev => prev + 1)  // trigger heatmap refetch
    };

    const handleDeleteHabit = async (habitId) => {
        if (!confirm('Delete this habit? This cannot be undone.')) {
            return
        }

        try {
            const response = await apiFetch(`${API_URL}/habits/${habitId}`, {
                method: 'DELETE',
            })

            if (response.status === 204) {
                setHabits(prev => prev.filter(h => h.id !== habitId))
            }
        } catch(error) {
            console.log('Error deleting habit', error)
        }
    }

    return(
        <div className='dashboard'>
            <h1>Dashboard</h1>
            <button className='logout-button' onClick={onLogout}>Log Out</button>
            <p>{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</p>
            <DailyQuote />

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
                {error && <p className="error-message">{error}</p>}
            </div>
            {habits.map((habit) => (
                <div key={habit.id} className="habit-card">
                    <div className="habit-card-header" onClick={() => 
                        setExpandedHabitId(expandedHabitId === habit.id ? null : habit.id)
                    }>
                        <input 
                            type="checkbox" 
                            checked={habit.completed_on_date || false} 
                            onChange={(e) => {
                                e.stopPropagation()
                                toggleHabit(habit.id)
                            }}
                            onClick={(e) => e.stopPropagation()}
                        />
                        <div className="habit-card-content">
                            <h2>{habit.name}</h2>
                            <p>{habit.schedule_type} · Target: {habit.target_count}</p>
                            {habit.notes && <p>{habit.notes}</p>}
                        </div>
                        <button 
                            className="delete-habit-button" 
                            onClick={(e) => {
                                e.stopPropagation()
                                handleDeleteHabit(habit.id)
                            }}
                        >
                            Delete
                        </button>
                    </div>
                    {expandedHabitId === habit.id && (
                        <div className="habit-heatmap">
                            <HabitHeatmap habitId={habit.id} refreshKey={heatmapRefresh} />
                        </div>
                    )}
                </div>
            ))}
        </div>
    )
}

export default Dashboard