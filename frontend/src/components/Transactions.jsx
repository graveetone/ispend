import { DayPicker } from "react-day-picker";
import { useEffect, useState } from "react";
import "react-day-picker/style.css";
import { fetchTransactions } from "./../api"

export default function Transactions() {
  const [selected, setSelected] = useState(new Date());
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);

  
  useEffect(() => {
      setLoading(true)
      const loadDayTransactions = async () => {
          const monthStr = selected.toLocaleDateString('en-CA');
          const data = await fetchTransactions({date: monthStr})
    
          setTransactions(data);
      };

    loadDayTransactions()
    setTimeout(() => {setLoading(false)}, 0)
    
    }, [selected])

  return (
    <div className="flex flex-col w-[90%] border-blue-500  gap-5">
        <div className="flex justify-center items-center border-red-500 w-full" >
            <DayPicker primaryColor={"red"} mode="single" month={selected} selected={selected} onMonthChange={setSelected} onSelect={setSelected} classNames={{chevron: "fill-red-500", today: "outline outline-1 outline-red-500 rounded-full", selected: "text-white bg-red-500 rounded-full",}}/>
        </div>
        <div className="flex flex-col justify-center items-center  border-yellow-400"> 
          <table className="text-center border-green-300 w-full">
            <thead className="bg-red-500">
              <tr className="">
                <th className="p-1 font-normal">Category</th>
                <th className="p-1 font-normal">Description</th>
              </tr>
            </thead>
            <tbody className="">
            {loading ? (
                <tr>
                  <td className="p-3" colSpan={2}>
                    <div className="flex justify-center">
                        <img className ="w-[30%]" src="https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyOXM4bTk5cm00ZmI3dzMyaWxoOTNjYWx2YnN2M2R6ejh6Y2xjamU5MCZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/mPaNqi4mmXJKCYX18R/source.gif"/>
                    </div>
                  </td>
                </tr>
            ) : (
            transactions.length === 0) ? (
                <tr>
                    <td className="p-3 text-center text-slate-500" colSpan={2}>
                    No data
                    </td>
                </tr>
                ) : (
              transactions.map((item, index) => (
                <tr key={index} className={` text-white `}>
                    <td className="p-1 font-normal border border-white">{item.category}</td>
                    {item.type === "expense" && <td className="p-1 font-normal border border-white"><span className="text-red-500">Spent</span> {item.amount} <span className="text-red-500">on</span> {item.description}</td>}
                    {item.type === "income" && <td className="p-1 font-normal border border-white"><span className="text-green-500">Received</span> {item.amount} <span className="text-green-500">from</span> {item.description}</td>}
                </tr>
              )))}
            </tbody>
          </table>
        </div> 
    </div>
  );
}
