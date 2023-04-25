import React from 'react'
import './HitScreen.css'
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { Link } from 'react-router-dom'
import HitTable from './HitTable.js'

const HitScreen = () => {
  return (
    <>
      <div className='navBar'>
        <Link to='/'>
            <button type='button' className="btn btn-outline-danger" style={{marginRight: '10px'}}>Home</button>
        </Link>
        <Link to='/memory'>
          <button type="button" class="btn btn-outline-primary" style={{ marginRight: '10px' }}>Memory</button>
        </Link>
        <Link to='/register'>
          <button type="button" class="btn btn-outline-secondary" style={{ marginRight: '10px' }}>Register</button>
        </Link>
        <Link to='/dataHazard'>
          <button type="button" class="btn btn-outline-success" style={{ marginRight: '10px' }}>Data Hazards</button>
        </Link>
        {/* <Link to='/controlHazards'>
          <button type="button" class="btn btn-outline-danger" style={{ marginRight: '10px' }}>Control Hazards</button>
        </Link> */}
        <Link to='/Hits'>
          <button type="button" class="btn btn-outline-success" style={{ marginRight: '10px' }}>Hits/Misses</button>
        </Link>
        <Link to='/dataCache'>
          <button type="button" class="btn btn-outline-secondary" style={{ marginRight: '10px' }}>Data Cache</button>
        </Link>
        <Link to='/instCache'>
          <button type="button" class="btn btn-outline-primary" style={{ marginRight: '10px' }}>Instruction Cache</button>
        </Link>
        <Link to='/simulator'>
          <button type='button' className="btn btn-outline-danger" style={{marginRight: '10px'}}> Simulation</button>
        </Link>
      </div>
      <div>
        <HitTable />
      </div>
    </>
  )
}

export default HitScreen
