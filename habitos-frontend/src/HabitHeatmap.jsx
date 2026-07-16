// habitos-frontend/src/HabitHeatmap.jsx

import { useState, useEffect } from 'react'
import CalendarHeatmap from 'react-calendar-heatmap'
import 'react-calendar-heatmap/dist/styles.css'
import { Tooltip } from 'react-tooltip'
import apiFetch from './apiFetch.js'

const API_URL = import.meta.env.VITE_API_URL

function HabitHeatmap({ habitId, refreshKey }) {
  const [values, setValues] = useState([])
  
  useEffect(() => {
    const fetchHistory = async () => {
        const response = await apiFetch(`${API_URL}/habits/${habitId}/history`)
        const data = await response.json()
        setValues(data)
    }
    fetchHistory()
  }, [habitId, refreshKey])
  
  const today = new Date()
  const startDate = new Date(today)
  startDate.setDate(today.getDate() - 365)
  
  return (
    <>
      <CalendarHeatmap
        startDate={startDate}
        endDate={today}
        values={values}
        classForValue={(value) => {
          if (!value) return 'color-empty'
          return 'color-completed'
        }}
        tooltipDataAttrs={(value) => {
          if (!value || !value.date) {
            return { 'data-tooltip-id': 'heatmap-tooltip', 'data-tooltip-content': 'No completion' }
          }
          return { 
            'data-tooltip-id': 'heatmap-tooltip', 
            'data-tooltip-content': `Completed on ${value.date}` 
          }
        }}
      />
      <Tooltip id="heatmap-tooltip" />
    </>
  )
}

export default HabitHeatmap