import React from 'react'
import { BrowserRouter, Routes, Route, Link, Outlet } from 'react-router-dom';
import Dashboard from './components/Dashboard'
import MonthCalendar from './components/Calendar'

export default function App() {
  return (
    <>
    {/* Navigation */}
    <nav>
      {/* <Link to="/">Dashboard</Link>
      <Link to="/calendar">Calendar</Link> */}
      {/* <Link to="/contact">Contact</Link> */}
    </nav>

    {/* Routes */}
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/calendar" element={<MonthCalendar />} />
      {/* <Route path="/contact" element={<Contact />} /> */}
    </Routes>

  </>
  )
}
