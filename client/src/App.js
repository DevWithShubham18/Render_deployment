import { useReducer } from 'react'
import axios from 'axios'
import './App.css'

const initialState = {
  file: null,
  status: "Waiting for upload...",
  question: "",
  insights: null
}

function reducer(state, action) {
  switch (action.type) {
    case "SET_FILE":
      return { ...state, file: action.payload }
    case "SET_STATUS":
      return { ...state, status: action.payload }
    case "SET_QUESTION":
      return { ...state, question: action.payload }
    case "SET_INSIGHTS":
      return { ...state, insights: action.payload }
    default:
      return state
  }
}

function App() {
  const [state, dispatch] = useReducer(reducer, initialState)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!state.file) return

    dispatch({ type: "SET_STATUS", payload: "Uploading and processing PDF..." })

    const formData = new FormData()
    formData.append("file", state.file)

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload", formData)
      dispatch({ type: "SET_STATUS", payload: response.data.message })
    } catch (error) {
      dispatch({ type: "SET_STATUS", payload: "Upload failed" })
    }
  }

  const handleQuery = async (e) => {
    e.preventDefault()
    if (!state.question) return

    dispatch({ type: "SET_STATUS", payload: "Analyzing..." })

    const formData = new FormData()
    formData.append("question", state.question)

    try {
      const response = await axios.post("http://127.0.0.1:8000/query", formData)
      if (response.data.success) {
        dispatch({ type: "SET_INSIGHTS", payload: response.data.data })
        dispatch({ type: "SET_STATUS", payload: "Analysis complete" })
      } else {
        dispatch({ type: "SET_STATUS", payload: "Query failed" })
      }
    } catch (error) {
      dispatch({ type: "SET_STATUS", payload: "Query failed" })
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '50px', fontFamily: 'sans-serif' }}>
      <h1>Company Report Analyzer</h1>

      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>Upload Report</h3>
        <input type="file" accept=".pdf" onChange={(e) => dispatch({ type: "SET_FILE", payload: e.target.files[0] })} />
        <button onClick={handleUpload} style={btnStyle}>Process Document</button>
      </div>

      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
        <h3>Ask Question</h3>
        <input
          type="text"
          placeholder="What was the total revenue?"
          value={state.question}
          onChange={(e) => dispatch({ type: "SET_QUESTION", payload: e.target.value })}
          style={{ width: '70%', padding: '10px', marginRight: '10px' }}
        />
        <button onClick={handleQuery} style={btnStyle}>Analyze</button>
      </div>

      <p style={{ marginTop: '20px', fontWeight: 'bold', color: '#555' }}>
        Status: {state.status}
      </p>

      {state.insights && (
        <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9fa', borderRadius: '8px' }}>
          <h2>Results</h2>
          <p><strong>Summary:</strong> {state.insights.summary}</p>
          <h4>Metrics:</h4>
          <ul>
            {state.insights.metrics.map((metric, index) => (
              <li key={index}>{metric}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

const btnStyle = {
  padding: '10px 20px',
  background: '#007bff',
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer'
}

export default App