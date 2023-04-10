import React from 'react'
import './Simulator.css'

const Simulator = () => {
    return (
        <>
            <div className='topbar'>
                Simulator
            </div>
            <div className='runButtons'>
                <button type="button" class="btn btn-outline-danger" style={{ marginRight: '40px', paddingLeft: '50px', paddingRight: '50px' }}>Step</button>
                <button type="button" class="btn btn-outline-danger" style={{ paddingLeft: '50px', paddingRight: '50px' }}>Prev</button>
            </div>
            <div className='outer'>
                <div className='inner'>
                    <b>hello world</b>
                </div>
                <div className='inner'>
                    <b>hello world</b>
                </div>
                <div className='inner'>
                    <b>hello world</b>
                </div>
                <div className='inner'>
                    <b>hello world</b>
                </div>
                <div className='inner'>
                    <b>hello world</b>
                </div>
            </div>
        </>
    )
}

export default Simulator
