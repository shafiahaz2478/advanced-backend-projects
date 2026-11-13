import {useState} from "react";
import Packages from "../components/Packages.jsx";
import Summary from "../components/Summary.jsx";
import {Navigate} from "react-router";

function Main({token,packages,summary}){

    if (token === ""){
          return <Navigate replace to="/login" />;
      }
    return (
    <>
      <Packages packages={packages} />
      <Summary summary={summary} />
    </>
  )
}

export default Main