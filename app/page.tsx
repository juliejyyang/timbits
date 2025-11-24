'use client';
import { useState } from 'react';
import './styling.css';

function SearchBar() {
  const [item, setSearchItem] = useState('') // const [state, setState] = useState(initialState)
  const [results, setResults] = useState([])

  const handleSearch=async (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchedItem = e.target.value
    setSearchItem(searchedItem)

    if (searchedItem.length < 2) { // dont search if user types less than 2 char
      setResults([]) // clear previous results
      return // exit the function early, don't run the search
    }

    try {
      const res = await fetch(`http://localhost:8000/api/search?item=${searchedItem}`) // res=response of the api call
      const items = await res.json() // Converts the response body from JSON string to JavaScript object/array, await waits for parsing to complete
      setResults(items) // Saves the items to state. Component re-renders and displays the results
    } catch (error){
      console.error('Search failed:', error)
    }
  }

    return (
    <div>
      <form onSubmit={(e) => e.preventDefault()}>
        <input type='text' placeholder='place your order!' className='input_box' value={item} onChange={handleSearch}/>
      </form>
      
      {/* Display search results */}
      {results.length > 0 && (
        <div className="search-results">
          {results.map((menuItem: any) => (
            <div key={menuItem.id} className="results-item">
              <span>{menuItem.name}</span>
              <span>{menuItem.calories} cal</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function MyOrder() {
  return (
    <div className="container">
      <h1>My order:</h1>
      <SearchBar />
    </div>
  )
}

function CurrentOrder() {
  return (
    <div className="container">
      <h1>Current Order...</h1>
    </div>
  )
}

function OrderHistory() {
  return (
    <div className="container">
      <h1>Order History</h1>
    </div>
  )
}

export default function MyNextFastAPIApp() {
  const titleStyle = {
    fontSize: '100px',
    paddingTop: '15px',
    paddingLeft: '15px'
  }
  return (
    <div>
      <h1 className="title" style={titleStyle}>Tim-Bits</h1>
      <MyOrder/>
      <CurrentOrder/>
      <OrderHistory/>
    </div>
  );
}