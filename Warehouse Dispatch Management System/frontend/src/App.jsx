import {useEffect, useState} from "react";
import PackageCard from "./components/PackageCard.jsx";
import Packages from "./components/Packages.jsx";
import Summary from "./components/Summary.jsx";

const API_URL = "http://localhost:8001"
function App() {
  const [packages,setPackages] = useState([])
  const [summary,setSummary] = useState([])
  useEffect(() => {
    fetch(API_URL + "/packages")
        .then((response) => response.json())
        .then((data) => setPackages(data))
        .then(() => fetch(API_URL + "/summary")
        .then((response) => response.json())
        .then((data) => setSummary(data)))
  }, []);
  return (
    <>
      <Packages packages={packages} />
      <Summary summary={summary} />
    </>
  )
}

export default App
