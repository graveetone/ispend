import React, { useEffect, useState } from 'react'
import TransactionForm from './TransactionForm'
import Menu from './Menu';

import MonthView from './MonthView'
import {
  fetchTransactions,
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

return (
      <div className="flex flex-col justify-center items-center w-full gap-3 mt-3 pt-3">
        <div className="border-pink-500 w-[80%]">
          <MonthView transactions={transactions}/>
        </div>
      </div>
  )
}
