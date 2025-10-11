import { useState, useEffect } from 'react'
import axios from "axios"
import Table from "./Table"
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

const getCurrentMonthDate = () => {
    const today = new Date();
    return new Date(today.getFullYear(), today.getMonth(), 1)
}

function MonthView() {
  // keep current date in state
  const [currentDate, setCurrentDate] = useState(getCurrentMonthDate());
  const [response, setResponse] = useState({});

  // go to previous month
  const handlePrev = () => {
    const prev = new Date(currentDate);
    prev.setMonth(currentDate.getMonth() - 1);
    setCurrentDate(prev);
  };

  // go to next month
  const handleNext = () => {
    const next = new Date(currentDate);
    next.setMonth(currentDate.getMonth() + 1);
    setCurrentDate(next);
  };

  // format month and year
  const monthString = currentDate.toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  useEffect(() => {
      const date = currentDate.toLocaleDateString("en-CA", {
        day: "numeric",
        month: "numeric",
        year: "numeric",
      });
    console.log(`Request to http://0.0.0.0:8000/api/v1/months/${date}`)
      axios.get(`http://0.0.0.0:8000/api/v1/months/${date}`)
        .then(response => {
            console.log(response.data)
            setResponse(response.data)
          })
          .catch(error => {
            console.error("Error fetching data:", error);
          });
  }, [currentDate])


  return (
      <>
        <div className="flex items-center gap-4">
          <button
            onClick={handlePrev}
            className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
          >
            &lt;
          </button>
          <span className="text-lg font-medium">{monthString}</span>
          <button
            onClick={handleNext}
            className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
          >
            &gt;
          </button>
        </div>
        <div style={containerStyle}>
        </div>
        <Table title="Expenses" data={response.expenses} />
        <Table title="Incomes" data={response.incomes} />
    </>
  );
}


export default MonthView;
