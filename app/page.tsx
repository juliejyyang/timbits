'use client';
import { useState, useEffect } from 'react';
import './styling.css';

type MenuItem = {
  id: number;
  name: string;
  calories: number;
};

type OrderItem = {
  id: number;
  name: string;
  calories: number;
  quantity: number;
}

type PastOrder = {
  id: number;
  created_at: string;
  total_calories: number;
  items: OrderItem[];
}

function SearchBar({ onItemClick }: { onItemClick: (item: any) => void }) {
  const [item, setSearchItem] = useState('')
  const [results, setResults] = useState([])

  const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchedItem = e.target.value
    setSearchItem(searchedItem)

    if (searchedItem.length < 2) {
      setResults([])
      return
    }

    try {
      const result = await fetch(`http://localhost:8000/api/search?item=${searchedItem}`)
      const items = await result.json()
      setResults(items)
    } catch (error){
      console.error('Search failed:', error)
    }
  }

  const handleItemClick = (menuItem: any) => {
    onItemClick(menuItem)
    setSearchItem('') // Clear search after adding
    setResults([]) // Clear results after adding
  }

  return (
    <div>
      <form onSubmit={(e) => e.preventDefault()}>
        <input type='text' placeholder='place your order!' className='input_box' value={item} onChange={handleSearch}/>
      </form>
      
      {results.length > 0 && (
        <div className="search-results">
          {results.map((menuItem: any) => (
            <div 
              key={menuItem.id} 
              className="results-item"
              onClick={() => handleItemClick(menuItem)}
              style={{ cursor: 'pointer' }}
            >
              <span>{menuItem.name}</span>
              <span>{menuItem.calories} cal</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function MyOrder({ onItemClick }: { onItemClick: (item: any) => void }) {
  return (
    <div className="container">
      <h1>My order:</h1>
      <SearchBar onItemClick={onItemClick}/>
    </div>
  )
}

function CurrentOrder({ 
  orderItems, 
  totalCals, 
  onOrderSaved 
}: { 
  orderItems: MenuItem[];
  totalCals: number;
  onOrderSaved: () => void;
}) {
  async function handleSave() {
    if (orderItems.length === 0) {
      alert('Add items to your order first!');
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/api/orders', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          items: orderItems.map(item => ({
            name: item.name,
            calories: item.calories,
            quantity: 1
          })),
          total_calories: totalCals
        })
      });

      if (!res.ok) {
        throw new Error('Failed to save order');
      }

      const data = await res.json();
      alert('Order saved!');
      onOrderSaved();
    } catch (error) {
      console.error('Failed to save order: ', error);
      alert('Failed to save order');
    }
  }

  return (
    <div className="container">
      <h1>Current Order</h1>
      <ul id="orderlist">
        {orderItems.map((item, index) => (
          <li key={index} className="results-item">
            <span>{item.name}</span>
            <span>{item.calories} cal</span>
          </li>
        ))}
      </ul>
      <div>Total calories: {totalCals}</div>
      <button onClick={handleSave}>Save order</button>
    </div>
  )
}

function OrderHistory({ orders }: { orders: PastOrder[] }) {
  return (
    <div className="container">
      <h1>Order History</h1>
      {orders.length === 0 ? (
        <p>No past orders yet</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} className="past-order" style={{ 
            marginBottom: '20px', 
            padding: '15px', 
            border: '1px solid #ccc',
            borderRadius: '8px'
          }}>
            <h3>Order #{order.id}</h3>
            <p><strong>Date:</strong> {new Date(order.created_at).toLocaleString()}</p>
            <p><strong>Total Calories:</strong> {order.total_calories}</p>
            <h4>Items:</h4>
            <ul>
              {order.items.map((item) => (
                <li key={item.id}>
                  {item.name} - {item.calories} cal (x{item.quantity})
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  )
}

export default function MyNextFastAPIApp() {
  const [orderItems, setOrderItems] = useState<MenuItem[]>([]);
  const [totalCals, setTotalCals] = useState(0);
  const [pastOrders, setPastOrders] = useState<PastOrder[]>([]);

  function handleSetTotalCals(cals: number) {
    setTotalCals((prev) => prev + cals);
  }

  // Fetch order history on component mount
  const fetchOrderHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/orders');
      const data = await res.json();
      setPastOrders(data);
    } catch (error) {
      console.error('Failed to fetch order history:', error);
    }
  };

  useEffect(() => {
    fetchOrderHistory();
  }, []);

  const handleOrder = (menuItem: MenuItem) => {
    setOrderItems((prev) => [...prev, menuItem]);
    handleSetTotalCals(menuItem.calories ?? 0);
  }

  const handleOrderSaved = () => {
    // Clear current order
    setOrderItems([]);
    setTotalCals(0);
    // Refresh order history
    fetchOrderHistory();
  }

  const titleStyle = {
    fontSize: '100px',
    paddingTop: '15px',
    paddingLeft: '15px'
  }
  
  return (
    <div>
      <h1 className="title" style={titleStyle}>Tim-Bits</h1>
      <MyOrder onItemClick={handleOrder}/>
      <CurrentOrder orderItems={orderItems} totalCals={totalCals} onOrderSaved={handleOrderSaved}/>
      <OrderHistory orders={pastOrders}/>
    </div>
  );
}