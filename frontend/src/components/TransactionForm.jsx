import React, { useEffect, useState } from 'react'
import { createTransaction, getCategories } from "./../api"
import EditableSelect from "./EditableSelect"

export default function TransactionForm() {
  const [type, setType] = useState('expense')
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('')
  const [createdAt, setCreatedAt] = useState(new Date().toLocaleDateString('en-CA'))
  const [categories, setCategories] = useState([])

  const submit = async (e) => {
    e.preventDefault()
    if (!amount || !description || !category || !createdAt) return
    await createTransaction({ type, amount: parseFloat(amount), description, category, created_at: createdAt })
    setAmount('')
    setDescription('')
    setCategory('')
    setCreatedAt(new Date().toLocaleDateString('en-CA'))
    if (type === "expense") {
      alert(`Added ${type}: ${amount} on ${category}`)
    }
    else {
      alert(`Added ${type}: ${amount} from ${category}`)
    }
  }

  const expenseTransaction = (type === 'expense');
  
  useEffect(() => {
    async function getCategoriesAsync() {
      setCategories(["Other", ...await getCategories(type)])
    }
    getCategoriesAsync()
  }, [type])

  function Button({icon, caption}) {
    return (
      <button className="flex text-lg justify-center items-center p-3 gap-3 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500">
        <span>{icon}</span>
        <span>{caption}</span>
      </button>
    )
  }

  return (
    <form onSubmit={submit}>
      <div className='text-white flex flex-col gap-6 w-full'>
        <div className="flex gap-2 justify-around">
        <label className="inline-flex items-center cursor-pointer">
        <span className={`select-none text-xl font-medium text-heading ${expenseTransaction ? 'text-gray-400' : 'text-white'}`}>Expense</span>
        <input type="checkbox" className="sr-only peer" checked={!expenseTransaction} onChange={() => setType(expenseTransaction ? 'income' : 'expense')}/>
        <div className="relative mx-3 w-9 h-5 bg-red-500 peer-checked:bg-green-500 peer-focus:outline-none dark:peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-soft rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-buffer after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand"></div>
        <span className={`select-none text-xl font-medium text-heading ${!expenseTransaction ? 'text-gray-400' : 'text-white'}`}>Income</span>
        </label>
        </div>

        <div className='text-black border-purple-500 flex flex-col gap-3 w-full'>
          <input type="number" className="rounded-3xl" placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} />
          <input className="rounded-3xl" placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
          <EditableSelect className="rounded-3xl" value={category} options={categories} onCreate={setCategory} onChange={setCategory} placeholder={"Category"} />
          <input type="date" className="rounded-3xl" value={createdAt} onChange={e => setCreatedAt(e.target.value)} />
        </div>

        <Button icon="💵" caption="Add transaction" />
      </div>
    </form>
  )
}
