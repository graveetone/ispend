import { DayPicker } from "react-day-picker";
import { useEffect, useState } from "react";
import "react-day-picker/style.css";
import { fetchTransactions } from "./../api"
import { Link } from "react-router-dom";

export default function MonthCalendar() {
  const [selected, setSelected] = useState(new Date());
  const [transactions, setTransactions] = useState([]);

  
  useEffect(() => {
      const loadDayTransactions = async () => {
          const monthStr = selected.toLocaleDateString('en-CA');
          const data = await fetchTransactions({date: monthStr})
    
          setTransactions(data);
      };

    loadDayTransactions()
    }, [selected])

  return (
    <div className="flex flex-col items-center">
    <div className="flex justify-around w-full p-6 items-center  border-red-500">
        <div className="flex justify-center items-center  border-red-500 w-full" >
            <DayPicker mode="single" month={selected} selected={selected} onSelect={setSelected}/>
        </div>
        <div className=" border-red-500 w-full flex flex-col justify-center items-center h-[80vh]">
            {transactions.length > 0 ? (
                <table>
                    <thead className="bg-red-500">
                        <tr>
                            <th className="border p-4">Category</th>
                            <th className="border p-4">Amount</th>
                            <th className="border p-4">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map((tx, index) => (
                            <tr key={index} className={`text-black ${tx.type === 'expense' ? 'bg-red-200' : 'bg-green-200'}`}>
                                <td className="border p-4">{tx.category}</td>
                                <td className="border p-4">{tx.type === "expense" ? "-" : "+"} {tx.amount}</td>
                                <td className="border p-4">{tx.description}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : `No transactions for ${selected.toLocaleDateString()}`}
        </div>
    </div>
    <div className="flex">
        <Link className="px-4 py-2 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500" to="/">📌 Dashboard</Link>
    </div>
    </div>
  );
}