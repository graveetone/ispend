import { useState, useEffect } from 'react'
import axios from "axios"
import Table from "./Table"
import MonthView from "./MonthView"
// import './App.css'

const bordered = {
    border: "white 1px solid"
}
  const containerStyle = {
    display: "flex",
    justifyContent: "space-around",
    border: "1px red solid",
//     border: "white 1px solid"

    padding: "20px",
//     gap: "10px",
//     alignItems: "center",
  };


function MainPage() {
//   const [expenses, setExpenses] = useState([])
//   const [incomes, setIncomes] = useState([])

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
  return (
    <>
        <MonthView/>
{/*         <div style={containerStyle}> */}
{/*             <Table title="Expenses" data={expenses}/> */}
{/*             <Table title="Incomes" data={incomes}/> */}
{/*         </div> */}
    </>
  )
}

export default MainPage
