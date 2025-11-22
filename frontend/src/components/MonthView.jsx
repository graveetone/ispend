import { useState, useEffect } from "react";
import dayjs from "dayjs";
import {getMonthTransactions} from "./../api"

export default function MonthView({transactions}) {
  const [month, setMonth] = useState(dayjs().startOf("month"));
  const [data, setData] = useState({
    expenses: [],
    incomes: [],
  });

  useEffect(() => {
    const loadMonth = async () => {
      const monthStr = month.format("YYYY-MM-DD");
      const data = await getMonthTransactions(monthStr)

      setData(data);
    };

    loadMonth();
  }, [month, transactions]);


  const prevMonth = () => {
    setMonth(month.subtract(1, "month"));
  };

  const nextMonth = () => {
    setMonth(month.add(1, "month"));
  };

  return (
    <div className="p-6 w-full flex flex-col items-around">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={prevMonth}
          className="px-3 py-2 bg-black text-white hover:text-white rounded-lg hover:bg-red-500 border border-2 border-red-500"
        >
          ← Prev
        </button>

        <h1 className="text-2xl font-semibold">
          {month.format("MMMM YYYY")}
        </h1>

        <button
          onClick={nextMonth}
          className="px-3 py-2 bg-black text-white hover:text-white rounded-lg hover:bg-red-500 border border-2 border-red-500"
        >
          Next →
        </button>
      </div>

      {/* Expenses */}
      <div className="mb-10">
        <h2 className="text-xl font-semibold mb-3">Expenses</h2>
        <table className="w-full text-left">
          <thead className="bg-red-500">
            <tr>
              <th className="border p-4">Category</th>
              <th className="border p-4">Amount</th>
              <th className="border p-4">Planned</th>
            </tr>
          </thead>
          <tbody className="">
            {data.expenses.map((item, idx) => (
              <tr key={idx} className="">
                <td className="border p-2">{item.category}</td>
                <td className="border p-2">{item.actual?.toFixed(2)}</td>
                <td className="border p-2">{item.planned?.toFixed(2)}</td>
              </tr>
            ))}

            {data.expenses.length === 0 && (
              <tr>
                <td className="p-3 text-center text-slate-500" colSpan={3}>
                  No data
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Incomes */}
      <div>
        <h2 className="text-xl font-semibold mb-3">Incomes</h2>
        <table className="w-full text-left">
          <thead className="bg-red-500">
            <tr>
              <th className="border p-2">Category</th>
              <th className="border p-2">Amount</th>
              <th className="border p-2">Planned</th>
            </tr>
          </thead>
          <tbody>
            {data.incomes.map((item, idx) => (
              <tr key={idx} className="">
                <td className="border p-2">{item.category}</td>
                <td className="border p-2">{item.actual?.toFixed(2)}</td>
                <td className="border p-2">{item.planned?.toFixed(2)}</td>
              </tr>
            ))}

            {data.incomes.length === 0 && (
              <tr>
                <td className="p-3 text-center text-slate-500" colSpan={3}>
                  No data
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
