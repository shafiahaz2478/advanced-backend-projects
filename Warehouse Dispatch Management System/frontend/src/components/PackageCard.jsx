


function PackageCard({packagee}){




    return <>
        <p>name: {packagee.name}</p>
        <p>destination: {packagee.destination}</p>
        <p>weight: {packagee.weight}</p>
        <p>arrival date: {packagee.arrival_date}</p>
    </>

}

export default PackageCard