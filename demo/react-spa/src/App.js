import React, { useState } from 'react';
import './App.css';

function App() {
  const [ resp, changeResponse ] = useState(null);
  const [ username, changeUsername ] =  useState('');
  const [ password, changePassword ] =  useState('');

  function onSubmit(e) {
     e.preventDefault();
    return fetch('http://localhost:8000/dj-rest-auth/login/', {
      method: 'POST',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body:  JSON.stringify({username, password})
    }).then(resp => resp.json()).then(data => {
      changeResponse(data)
    }).catch(error => console.log('error ->', error))
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Login
        </h1>
        <div className={'help-text'}>
          Inspect the network requests in your browser to view headers returned by dj-rest-auth.
        </div>
        <div>
          {resp &&
            <div className={'response'}>
              <code>
                {JSON.stringify(resp)}
              </code>
            </div>
          }
        </div>
        <div>
        <form onSubmit={onSubmit}>
          <div>
            <input
              onChange={(e) => changeUsername(e.target.value)}
              value={username}
              type={'input'}
              name={'username'}/>
          </div>
          <div>
            <input
              onChange={(e) => changePassword(e.target.value)}
              value={password}
              type={'password'}
              name={'password'}/>
          </div>
          <button type={'submit'}>Submit</button>
        </form>
        </div>
      </header>
    </div>
  );
}

export default App;
