import React, {useEffect} from 'react'

export const Company = (props) => {


    /*useEffect(() => {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            //body: JSON.stringify({"symbol": value})
        };

        fetch('/inside-trader', requestOptions)
            .then(response => response.json())
            .then(data => {})
            .catch(console.log)
    }, []);
*/
    return (
        <div><h3>Symbol: {props.location.state.symbol}</h3></div>
    );
};
