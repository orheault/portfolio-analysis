import { Menu } from "semantic-ui-react"
import { SearchTicker } from "./SearchTicker"

export const TopMenu = (props) => {
    const onToggleMenu = () => {
        console.log("menu toggle")
    }
    
    return (
        <div className="ui top inverted attached menu">
            <span className="item link grey"
                onClick={props.onToggleMenu}>Menu</span>

                <Menu.Menu position='right'>
                    <SearchTicker />
               </Menu.Menu>
        </div>
    )
}