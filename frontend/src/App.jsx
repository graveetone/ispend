import React from 'react'
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard'
import MonthCalendar from './components/Calendar'

export default function App() {
  return (
    <>
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/calendar" element={<MonthCalendar />} />
    </Routes>

  </>
  )
}
