import React, { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard'
import Transactions from './components/Transactions'
import Menu from './components/Menu';
import TransactionForm from './components/TransactionForm';
import { getAppVersion } from './api';

export default function App() {
  const [appVersion, setAppVersion] = useState({})
  const [appVersionVisible, setAppVersionVisible] = useState(false)
  useEffect(() => {
    async function getVersion() {
      setAppVersion(await getAppVersion())
    }
    getVersion()
  }, [])

  return (
    <div className='w-full flex justify-center items-center border-blue-400'>
      <div className='w-full sm:w-[80%] md:w-[70%] lg:w-[60%] xl:w-[50%] flex flex-col mt-3 mb-20 justify-center items-center gap-3 border-yellow-300'>
        <h1 className="text-3xl font-bold" onClick={() => setAppVersionVisible(!appVersionVisible)}>💰 iSpend 💰</h1>
        {appVersionVisible && <h2 className="text-sm font-thin">🤖 {appVersion.version} ({appVersion.commit}) 🤖</h2>}

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
