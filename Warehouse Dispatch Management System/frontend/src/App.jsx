import {useEffect, useState} from "react";
import { Routes, Route, Link } from "react-router"
import Main from "./pages/Main.jsx";
import Login from "./pages/Login.jsx";

const API_URL = "http://localhost:8001"
function App() {
    const [packages,setPackages] = useState([])
    const [summary,setSummary] = useState([])
    const [token , setToken] = useState("")
    const [refresh , setRefresh] = useState("")
    const [authed, setAuthed] = useState(false)



    function login(username , password){

      fetch(API_URL + "/logic", {
          method : 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
              "username":username,
              "password":password
          }),
      })
        .then((response) =>{if (response.ok){setAuthed(true)} return response.json()})
        .then((data) => {setToken(data.access_token) ; setRefresh(data.refresh_token)})



  }

  function updatePackage(){
      fetch(API_URL + "/packages" , {
          headers : {
              'token' : token
          }
      })
        .then((response) => response.json())
        .then((data) => setPackages(data))

  }

  function updateSummary(){
      fetch(API_URL + "/summary" , {
          headers : {
              'token' : token
          }
      })
        .then((response) => { if (response.status === 401) {updateToken(); throw Error} return response.json()})
        .then((data) => setSummary(data))
          .catch((err) => updateToken())
  }

  function updateToken(){
    fetch(API_URL + "/refresh" , {
          headers : {
              'token' : token
          }
      })
        .then((response) => response.json())
        .then((data) => setToken(data.access_token))
  }

  useEffect(() => {
      if (token){
          updatePackage()
          updateSummary()
      }

  }, [token])


  return (
    <>
    <nav>
      <Link to="/">Main</Link>
    </nav>
    <Routes>
        <Route path="/" element={<Main token={token} packages={packages} summary={summary}/>} />
        <Route path="/login" element={<Login login={login} authed={authed}/>} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
    </Routes>
    </>
  )
}

export default App
