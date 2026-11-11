import PackageCard from "./PackageCard.jsx";


function Packages({packages}){

 return <>
        <h2>Packages</h2>

    <div className="package">
        {packages.map((packagee) => {return <PackageCard key={packagee.id} packagee={packagee}/>})}
    </div>

 </>
}

export default Packages