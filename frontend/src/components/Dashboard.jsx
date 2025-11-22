import React, { useEffect, useState } from 'react'
import TransactionForm from './TransactionForm'

import { Link } from 'react-router-dom';
import MonthView from './MonthView'
import {
  fetchTransactions,
  createTransaction,
} from './../api'

export default function Dashboard() {
    const [transactions, setTransactions] = useState([])

    useEffect(() => {
      const load = async () => {
        try {
          const res = await fetchTransactions()
          setTransactions(res)
        } catch (e) {
          console.error(e)
          alert('Error loading transactions')
        }
      }
      
      load()
    }, [])
    const handleCreate = async (payload) => {
      const t = await createTransaction(payload)
      setTransactions(prev => [t, ...prev])
      return t
    }

return (
    <div className="w-full p-8 border-blue-500 h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">💰 iSpend 💰</h1>

      <div className="flex justify-around border-white h-full">
        <div className="w-[50%] border-yellow-500">
          <MonthView transactions={transactions}/>
        </div>
        <div className="w-[25%] border-green-500 flex flex-col gap-4">
          <TransactionForm onCreate={handleCreate} />
        </div>
      </div>
      <div className="flex justify-end">
          <Link className="px-4 py-2 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500" to="/calendar">📆 Calendar</Link>
      </div>
    </div>
  )
}
