import {BrowserRouter as Router, Link, NavLink} from 'react-router-dom';

export const SideMenuVertical = (props) => {

    return (
        <div style={{backgroundColor: "#2a3042", paddingTop: 65}}
             className={`ui left vertical menu sidebar inverted borderless thin ${props.toggle ? 'visible' : ''}`}>

            <div className={"menu-title"}>MENU</div>

            <NavLink to='/' exact className={"item link"} activeClassName={"active"}>
                <div className="centered menu-item">Overview</div>
            </NavLink>
            <NavLink to='/board' exact className={"item link"} activeClassName={"active"}>
                <div className="centered menu-item">Board</div>
            </NavLink>
            <NavLink to='/watch-list' exact className={"item link"} activeClassName={"active"}>
                <div className="centered menu-item">Watch List</div>
            </NavLink>
            <NavLink to='/insider-trading' exact className={"item link"} activeClassName={"active"}>
                <div className="centered menu-item">Insider Trading</div>
            </NavLink>


            <div className={"menu-title"}>SETTINGS</div>

            <Link to='/alert' className={"item link"}>
                <div className="centered menu-item">Alert</div>
            </Link>
        </div>

    )
} 