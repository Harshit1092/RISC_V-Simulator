import React from 'react'
import './App.css';
import MemoryScreen from './Components/MemoryScreen.js'
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Input from './Components/input.js'

const App = () => {
  return (
    <div className='App'>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Input />} />
        <Route path='/memory' element={<MemoryScreen />} />
      </Routes>
      </BrowserRouter>
      {/* <MemoryScreen /> */}
    </div>
  )
}

export default App
