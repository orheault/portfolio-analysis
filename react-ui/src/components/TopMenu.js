import {Icon, Menu} from "semantic-ui-react"
import { SearchTicker } from "./SearchTicker"

export const TopMenu = (props) => {
    return (
        <div className="ui top attached menu borderless">
            <div className="item" onClick={props.onToggleMenu}>
                <Icon name='sidebar' size='large' className='link' />
            </div>
            <SearchTicker className='item' />
        </div>
    )
}