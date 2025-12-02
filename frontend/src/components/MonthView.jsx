import { useState, useEffect } from "react";
import dayjs from "dayjs";
import {getMonthTransactions, editPlan} from "./../api"


export default function MonthView({transactions}) {
  const [month, setMonth] = useState(dayjs().startOf("month"));
  const [data, setData] = useState({
    expenses: [],
    incomes: [],
    total: {}
  });
  const [planEdited, setPlanEdited] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleDoubleClick(element) {
    let result = prompt(`Set planned amount for ${element.category} (${month.format("MMMM YYYY")})`);

    if (element.planned && element.planned === result) return;

    await editPlan({
      category: element.category,
      type: element.type,
      month: month.format("YYYY-MM-DD"),
      amount: parseFloat(result)
    })
    setPlanEdited(true)

  }

  useEffect(() => {
    setLoading(true)
    const loadMonth = async () => {
      const monthStr = month.format("YYYY-MM-DD");
      const data = await getMonthTransactions(monthStr)

      setData(data);
      setPlanEdited(false) // this shit triggers useEffect again
    };

    loadMonth();
    setTimeout(() => {setLoading(false)}, 0)
  }, [month, transactions, planEdited]);


  const prevMonth = () => {
    setMonth(month.subtract(1, "month"));
  };

  const nextMonth = () => {
    setMonth(month.add(1, "month"));
  };

  function MonthViewHeader() {
    return (
      <div className="flex items-center justify-around">
        <button
          onClick={prevMonth}
          className="w-full p-1 bg-black text-lg text-white hover:text-white rounded-lg hover:bg-red-500 border border-2 border-red-500"
        >
          ◀ Previous
        </button>

        <div className="w-full flex flex-col justify-center items-center" onDoubleClick={() => setMonth(dayjs().startOf("month"))}>
          <h3 className="text-md font-semibold">
            {month.format("MMMM")}
          </h3>
          <h3 className="text-md font-semibold">
            {month.format("YYYY")}
          </h3>
        </div>

        <button
          onClick={nextMonth}
          className="w-full p-1 bg-black text-lg text-white hover:text-white rounded-lg hover:bg-red-500 border border-2 border-red-500"
        >
          Next ▶
        </button>
      </div>
    )
  }
  function MonthViewTable({title, data, total}) {
    return (
      <div className="flex flex-col justify-center items-center gap-3">
      <h2 className="text-xl font-medium">{title}</h2>
      <table className="w-full text-left">
        <thead className="bg-red-500">
          <tr className="text-center">
            <th className="p-1 font-normal">Category</th>
            <th className="p-1 font-normal">Amount</th>
            <th className="p-1 font-normal">Planned</th>
            <th className="p-1 font-normal">Diff</th>
          </tr>
        </thead>
        <tbody className="">
          {loading ? (
            <tr>
            <td className="p-3" colSpan={4}>
              <div className="flex justify-center">
                  <img className ="w-[30%]" src="https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyOXM4bTk5cm00ZmI3dzMyaWxoOTNjYWx2YnN2M2R6ejh6Y2xjamU5MCZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/mPaNqi4mmXJKCYX18R/source.gif"/>
              </div>
            </td>
          </tr> ) : (
            data.length === 0 ? (
              <tr>
                <td className="p-3 text-center text-slate-500" colSpan={4}>
                  No data
                </td>
              </tr>
            ) : (
              <>
              <tr key={`total_actual_${title}`} className="text-center bg-white text-red-500">
                <td className="p-1 font-bold border">Total</td>
                <td className="p-1 font-bold border">{total.actual.toFixed(2)}</td>
                <td className="p-1 font-bold border">{total.planned.toFixed(2)}</td>
                <td className={`p-1 font-bold border ${total.planned.toFixed(2) - total.actual.toFixed(2) > 0 ? 'text-green-500' : 'text-red-500'}`}>{(total.planned - total.actual).toFixed(2)}</td>
              </tr>
              {data.map((item, idx) => (
                <tr key={idx} className="text-center">
                  <td className="p-1 font-normal border">{item.category}</td>
                  <td className="p-1 font-normal border">{item.actual?.toFixed(2)}</td>
                  <td className="p-1 font-normal border" onDoubleClick={() => handleDoubleClick(item)  }> {item.planned?.toFixed(2)} </td>
                  <td className={`p-1 font-normal border ${item.planned?.toFixed(2) - item.actual?.toFixed(2) > 0 ? 'text-green-500' : 'text-red-500'}`}> {Number.isNaN(item.planned?.toFixed(2) - item.actual?.toFixed(2)) ? "" : (item.planned?.toFixed(2) - item.actual?.toFixed(2)).toFixed(2)} </td>
                </tr>
              ))}
            </>
            ))}
        </tbody>
      </table>
    </div>
    )
  }
  return (
    <div className="w-full flex flex-col items-around border-yellow-400 gap-5">
      <MonthViewHeader />
      <MonthViewTable title="Expenses" data={data.expenses} total={data.total.expenses}/>
      <MonthViewTable title="Incomes" data={data.incomes} total={data.total.incomes}/>
      </div>
  )
}
