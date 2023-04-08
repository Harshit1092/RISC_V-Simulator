import React from 'react'
import './RegisterScreen.css'
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import RegisterTable from './RegisterTable.js'

const RegisterScreen = () => {
  return (
    <>
    <div className='navBar'>
    <button type="button" class="btn btn-outline-primary" style={{marginRight:'10px'}}>Primary</button>
    <button type="button" class="btn btn-outline-secondary" style={{marginRight:'10px'}}>Secondary</button>
    <button type="button" class="btn btn-outline-success" style={{marginRight:'10px'}}>Success</button>
    <button type="button" class="btn btn-outline-danger" style={{marginRight:'10px'}}>Danger</button>
    </div>
    <div>
    <RegisterTable />
    </div>
    </>
  )
}

export default RegisterScreen
