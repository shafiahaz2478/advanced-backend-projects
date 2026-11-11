function Summary({summary}){

    return <>
        <h2>Summary</h2>
        <p>package received: {summary.package_received}</p>
        <p>package pending: {summary.package_pending}</p>
        <p>package dispatched: {summary.package_dispatched}</p>

    </>
}

export default Summary