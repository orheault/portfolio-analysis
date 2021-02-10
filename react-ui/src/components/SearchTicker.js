import { Search } from "semantic-ui-react"
import React from 'react'

export const SearchTicker = () => {

    function handleSearchChange(event){
        console.log(event.target.value)
    }

    return (
        <Search 
          onSearchChange={handleSearchChange}
          type='text'
        />
    )
}