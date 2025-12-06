import React from 'react'



import MonthView from './MonthView'

export default function Dashboard() {
return (
      <div className="flex flex-col justify-center items-center w-full gap-3 mt-3 pt-3">
        <div className="border-pink-500 w-[80%]">
          <MonthView />
        </div>
      </div>
  )
}
