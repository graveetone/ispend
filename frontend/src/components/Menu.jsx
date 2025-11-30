import { Link } from 'react-router-dom';


export default function Menu() {
    return (
        <div className='flex w-full mb-4 justify-between gap-3'>
        <h1 className="text-3xl font-bold">💰 iSpend 💰</h1>
        <div className='flex flex-end gap-3'>
          <Link className="px-4 py-2 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500" to="/">📌 Dashboard</Link>
          <Link className="px-4 py-2 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500" to="/transactions">📆 Transactions</Link>
        </div>
      </div>
    )
}