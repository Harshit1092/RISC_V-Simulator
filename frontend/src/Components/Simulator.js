import React from 'react'
import './Simulator.css'
import data from './cycle.json'
import {useState} from 'react'


const Simulator = () => {

    const [index, setIndex] = useState(0)
    
    function stepHandler() {
        setIndex(index+1)
    }

    function prevHandler() {
        setIndex(index-1)
    }

    return (
        <>
            <div className='topbar'>
                Simulator
            </div>
            <div className='runButtons'>
                <button type="button" class="btn btn-outline-danger" style={{ marginRight: '40px', paddingLeft: '50px', paddingRight: '50px' }} onClick={stepHandler}>Step</button>
                <button type="button" class="btn btn-outline-danger" style={{ paddingLeft: '50px', paddingRight: '50px' }} onClick={prevHandler}>Prev</button>
            </div>
            <div className='outer'>
                <div className='inner'>
                    <b>{data[index]['fetch']}</b>
                </div>
                <div className='inner'>
                    <b>{data[index]['decode']}</b>
                </div>
                <div className='inner'>
                    <b>{data[index]['execute']}</b>
                </div>
                <div className='inner'>
                    <b>{data[index]['memory']}</b>
                </div>
                <div className='inner'>
                    <b>{data[index]['writeback']}</b>
                </div>
            </div>
        </>
    )
}

export default Simulator
