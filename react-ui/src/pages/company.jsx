import React from 'react'

export const Company = (props) => {
    return (
        <div><h3>Company {props.location.state.symbol}</h3></div>
    );
};
