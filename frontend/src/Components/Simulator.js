import { useEffect, useState } from 'react'
import './Simulator.css'
import data from './cycle.json'


const Simulator = () => {

    const [index, setIndex] = useState(0)
    
    useEffect(()=> {
        if(data[index]['fetch'] == -1){
            document.querySelector('.div1').classList.add('glow')
        }
        else{
            document.querySelector('.div1').classList.remove('glow')
        }

        if(data[index]['decode'] == -1){
            document.querySelector('.div2').classList.add('glow')
        }
        else{
            document.querySelector('.div2').classList.remove('glow')
        }

        if(data[index]['execute'] == -1){
            document.querySelector('.div3').classList.add('glow')
        }
        else{
            document.querySelector('.div3').classList.remove('glow')
        }

        if(data[index]['memory'] == -1){
            document.querySelector('.div4').classList.add('glow')
        }
        else{
            document.querySelector('.div4').classList.remove('glow')
        }

        if(data[index]['writeback'] == -1){
            document.querySelector('.div5').classList.add('glow')
        }
        else{
            document.querySelector('.div5').classList.remove('glow')
        }

    },[index])

    function stepHandler() {
        if(index < data.length) setIndex(index+1)
    }

    function prevHandler() {
        if(index >= 1) setIndex(index-1)
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
                <div className='inner div1'>
                    <b>{data[index]['fetch']}</b>
                </div>
                <div className='inner div2'>
                    <b>{data[index]['decode']}</b>
                </div>
                <div className='inner div3'>
                    <b>{data[index]['execute']}</b>
                </div>
                <div className='inner div4'>
                    <b>{data[index]['memory']}</b>
                </div>
                <div className='inner div5'>
                    <b>{data[index]['writeback']}</b>
                </div>
            </div>
        </>
    )
}

export default Simulator
