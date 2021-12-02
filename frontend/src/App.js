import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import axios from 'axios';


function App() {

    const [people, setPeople] = useState(initialState: [])

    useEffect(effect: () => {
        axios({
            method: "GET",
            url: "http://127.0.0.1:8000/api/test-api/"
        }).then(response => {
            setPeople(response.data)
        })
        }
    }, deps:[])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
