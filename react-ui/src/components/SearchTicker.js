import { Search } from "semantic-ui-react"
import React, {useState} from 'react'

export const SearchTicker = () => {
    const [state, setState] = useState({isLoading: false, results: [{ title: '', description: '' }], value: '' });

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

    const { isLoading, value, results } = state

    return (

        <Search
          onSearchChange={handleSearchChange}
          onResultSelect={handleResultSelect}
          type='text'
          loading={isLoading}
          results={results}
          value={value}
        />
    )
}













