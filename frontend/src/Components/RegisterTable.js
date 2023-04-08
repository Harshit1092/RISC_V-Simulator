import { useEffect } from "react";
// import RegisterData from "./RegisterData.js";
import RegisterData from './reg.json'

function RegisterTable(){
// get table column
 const column = Object.keys(RegisterData[0]);
 // get table heading data
 const ThData =()=>{
    
     return column.map((data)=>{
         return <th key={data} style={{width:'20%', textAlign:'center'}}>{data}</th>
     })
 }
// get table row data
const tdData =() =>{
   
     return RegisterData.map((data)=>{
       return(
           <tr>
                {
                   column.map((v)=>{
                       return <td style={{width:'20%', textAlign:'center'}}>{data[v]}</td>
                   })
                }
           </tr>
       )
     })
}
  return (
      <table className="table">
        <thead>
         <tr>{ThData()}</tr>
        </thead>
        <tbody>
        {tdData()}
        </tbody>
       </table>
  )
}
export default RegisterTable;