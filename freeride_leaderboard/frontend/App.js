import React, { Component } from 'react';
import './App.css';
import './practice/Table.css'

function App() {
  const [entries, setEntries] = React.useState(null);

  React.useEffect(() => {
  fetch("/api")
      .then((res) => res.json())
      .then((data) => setEntries(data));
  }, []);

  return (
    <div className="App">
      <div className="header">
        <img src="/freeride_logo_transparent.png" alt="biker going down mountain terrain logo" width="300" height="300"/>
      </div>
      <div>
        <table class="Table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Time</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {entries && entries.map((info, index) => {
              return (
                <tr>
                  <td>{index+1}</td>
                  <td>{info.name}</td>
                  <td>{info.time}</td>
                  <td>{info.collectibles}</td>
                  <td>{info.date}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App;
