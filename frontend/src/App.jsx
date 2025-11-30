import React from 'react'
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard'
import Transactions from './components/Transactions'
import Menu from './components/Menu';
import TransactionForm from './components/TransactionForm';

export default function App() {
  return (
    <div className='w-full flex justify-center items-center border-blue-400'>
      <div className='w-full sm:w-[80%] md:w-[70%] lg:w-[60%] xl:w-[50%] flex flex-col mt-3 mb-20 justify-center items-center gap-3 border-yellow-300'>
        <h1 className="text-3xl font-bold">💰 iSpend 💰</h1>
        <Menu />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/new" element={<TransactionForm />} />
        </Routes>
    </div>
    </div>
  )
}
