import { Search } from "semantic-ui-react"
import React, {useState} from 'react'

export const SearchTicker = () => {
    const [state, setState] = useState({isLoading: false, results: [{ title: '', description: '' }], value: '' });
    const { isLoading, value, results } = state


    /** DETECT INPUT KEYBOARD AND FOCUS SEARCH BAR. ALLOWS TO SEARCH TICKER WITHOUT HAVING TO FOCUS ON THE SEARCH
     *  BAR **/
    const searchInputRef = React.useCallback(node => {
        if(node != null){
            document.addEventListener('keypress', event => {
                if(!node.focused){
                    node.focus();
                    node.value = node.value + event.key;
                }
            })
        }
    }, []);




    const handleResultSelect = (e, { result }) => {
        setState({ value: result.title })
    }

    const handleSearchChange = React.useCallback((e, { value }) => {
        setState({ isLoading: true, value })

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "symbol": value })
        };

        fetch('/search', requestOptions)
            .then(response => response.json())
            .then(data => data.slice(0,5))
            .then(data => {
                let results = []
                data.forEach((security) => {
                    //console.log(security.symbol + " " + security.description)
                    let result = { title: security.symbol, description: security.description }
                    results.push(result);
                });

                setState({
                    isLoading: false,
                    results: results
                })
            })
            .catch(console.log)
    });

    return (
        <Search
            input={{ref: searchInputRef}}
            onSearchChange={handleSearchChange}
            onResultSelect={handleResultSelect}
            type='text'
            loading={isLoading}
            results={results}
            value={value}
        />
    )
}













