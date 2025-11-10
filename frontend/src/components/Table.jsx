import { useState, useEffect } from 'react'
import axios from "axios"
// import './App.css'

function Table({title, data}) {
//   const [incomes, setIncomes] = useState([])
//   const [expenses, setExpenses] = useState([])
//
//   useEffect(() => {
//       axios.get("http://0.0.0.0:8000/api/v1/transactions/")
//         .then(response => {
//             setTimeout(() => {
//                 setIncomes(response.data.filter(t => t.type == "income"))
//             }, 1500)
//             setTimeout(() => {
//                 setExpenses(response.data.filter(t => t.type == "expense"))
//             }, 2000)
//           })
//           .catch(error => {
//             console.error("Error fetching data:", error);
//           });
//   }, [])
  const containerStyle = {
      display: "flex",
    padding: "20px",
    gap: "10px",
    alignItems: "center",
  };
//     const data = [
//     { id: 1, name: "Alice", age: 25 },
//     { id: 2, name: "Bob", age: 30 },
//     { id: 3, name: "Charlie", age: 28 },
//   ];
console.log(data)
  return (
    <>
        <div>
          <h1>{title}</h1>
          <div className="">
              <table className="">
                <thead className="">
                  <tr>
                    <th className="border border-gray-300 px-4 py-2">Category</th>
                    <th className="border border-gray-300 px-4 py-2">Actual</th>
                    <th className="border border-gray-300 px-4 py-2">Planned</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.length > 0 ? data.map(row => (
                    <tr key={row.id}>
                      <td className="border border-gray-300 px-4 py-2">{row.category}</td>
                      <td className="border border-gray-300 px-4 py-2">{row.actual}</td>
                      <td className="border border-gray-300 px-4 py-2">{row.planned}</td>
                    </tr>
                  )) : <tr> <td className="border border-gray-300 px-4 py-2">No data</td>
                  <td className="border border-gray-300 px-4 py-2">No data</td>
                  <td className="border border-gray-300 px-4 py-2">No data</td></tr>}
                </tbody>
              </table>
            </div>
        </div>
    </>
  )
}

export default Table;
