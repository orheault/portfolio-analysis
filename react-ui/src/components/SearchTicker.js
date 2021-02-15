import {Button, Icon, Search} from "semantic-ui-react"
import React, {useState} from 'react'
import {NavLink, useHistory} from "react-router-dom";

export const SearchTicker = (props) => {
    const [state, setState] = useState({isLoading: false, results: [{title: '', description: ''}], value: ''});
    const {isLoading, value, results} = state
    const [symbols, setSymbol] = useState([]);
    const linkHistory = useHistory();


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

    const handleResultSelect = (e, {result}) => {
        setSymbol(symbols => [...symbols, result.title]);
        linkHistory.push("/company", {symbol: result.title});
    }

    const handleSearchChange = (e, {value}) => {
        setState({isLoading: true, value})

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"symbol": value})
        };

        fetch('/search-symbol', requestOptions)
            .then(response => response.json())
            .then(data => data.slice(0, 5))
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
        const index = symbols.indexOf(symbol);
        if (index > -1) {
            document.getElementById("button_open" + symbol).remove()
            document.getElementById("button_close" + symbol).remove()

            symbols.splice(index, 1);
            setSymbol(symbols);

            if (symbols.length > 0) {
                linkHistory.push("/company", {symbol: symbols[0]});
            } else {
                linkHistory.push("/");
            }
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
                <div key={"divbutton"+ symbol}>
                    <NavLink key={symbol}
                             to={{pathname: "/company", state: {symbol: symbol}}}
                             activeClassName={"active"}
                             isActive={(match, location) => {
                                 if (!match) {
                                     return false;
                                 }

                                 if (location.state.symbol === symbol) {
                                     return true;
                                 }
                             }}
                    >
                        <Button key={"button"+ symbol} id={"button_open" + symbol} className={"symbol-button"} size='medium'>
                            {symbol}
                        </Button>
                    </NavLink>

                    <Button  key={"icon"+ symbol} id={"button_close" + symbol} icon={"delete"}
                             className={"right symbol-button-close"} size='medium'
                             onClick={() => {handleRemoveSymbolButton(symbol)}}>
                    </Button>
                </div>
            ))}
        </div>
    )
}
