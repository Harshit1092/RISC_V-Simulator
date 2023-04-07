import React from 'react'
import './MemoryScreen.css'
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import MemoryTable from './MemoryTable.js'

const MemoryScreen = () => {
  return (
    <>
    <div className='navBar'>
    <button type="button" class="btn btn-outline-primary">Primary</button>
    <button type="button" class="btn btn-outline-secondary">Secondary</button>
    <button type="button" class="btn btn-outline-success">Success</button>
    <button type="button" class="btn btn-outline-danger">Danger</button>
    </div>
    <div>
    <MemoryTable />
    </div>
    </>
  )
}

export default MemoryScreen
