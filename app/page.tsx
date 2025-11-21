import './styling.css';

function MyOrder() {
  return (
    <div className="container">
      <h1 className="header">My Order</h1>
      <input type="text" className="input_box"/>
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