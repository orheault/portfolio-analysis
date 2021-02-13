import {Button, Icon, Search} from "semantic-ui-react"
import React, {useState} from 'react'
import {Link} from "react-router-dom";

export const SearchTicker = (props) => {
    const [state, setState] = useState({isLoading: false, results: [{title: '', description: ''}], value: ''});
    const {isLoading, value, results} = state

    const [symbols, setSymbol] = useState([]);


    /** DETECT INPUT KEYBOARD AND FOCUS SEARCH BAR. ALLOWS TO SEARCH TICKER WITHOUT HAVING TO FOCUS ON THE SEARCH
     *  BAR **/
    const searchInputRef = React.useCallback(node => {
        if (node != null) {
            document.addEventListener('keypress', event => {
                if (!node.focused) {
                    node.focus();
                    node.value = event.key;
                }
            })
        }
    }, []);


    const handleResultSelect = (e, { result }) => {
        setSymbol(symbols => {
            const list = [...symbols, result.title];
            return list;
        });
    }

    const handleSearchChange = (e, {value}) => {
        setState({isLoading: true, value})

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"symbol": value})
        };

        fetch('/search', requestOptions)
            .then(response => response.json())
            .then(data => data.slice(0,5))
            .then(data => {
                let results = []
                data.forEach((security) => {
                    let result = {title: security.symbol, description: security.description}
                    results.push(result);
                });

                setState({
                    isLoading: false,
                    results: results
                })
            })
            .catch(console.log)
    };

    const handleRemoveSymbolButton = (symbol) => {
        console.log(symbols);
        console.log("Removed symbol " + symbol);

        const index = symbols.indexOf(symbol);
        if (index > -1) {
            document.getElementById(symbol).remove()

            symbols.splice(index, 1);
            setSymbol(symbols);
        }
    }

    return (
        <div className={props.className}>
            <Search
                input={{ref: searchInputRef}}
                onSearchChange={handleSearchChange}
                onResultSelect={handleResultSelect}
                type='text'
                loading={isLoading}
                results={results}
                value={value}
                placeholder={"Search.."}
            />

            {symbols.map(symbol => (
                <Link key={symbol} to={{pathname: "/company", query: {symbol: symbol}}}>

                    <Button key={symbol} id={symbol} style={{marginLeft: 30}} size='large'>
                        {symbol}
                        <Icon name='delete' className={"right"} onClick={() => {
                            handleRemoveSymbolButton(symbol)
                        }}/>
                    </Button>
                </Link>

            ))}
        </div>
    )
}













