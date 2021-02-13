import {Icon, Menu} from "semantic-ui-react"
import { SearchTicker } from "./SearchTicker"

export const TopMenu = (props) => {
    return (
        <div className="ui top fixed menu borderless">
            <div className="item" onClick={props.toggle}>
                <Icon name='sidebar' size='large' className='link'/>
            </div>
            <SearchTicker className='item'/>
        </div>
    )
}