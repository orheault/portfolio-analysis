import {BrowserRouter as Router, Link} from 'react-router-dom';

export const SideMenuVertical = (props) => {

    return (
        <div style={{backgroundColor: "#2a3042", paddingTop: 65}}
             className={`ui left vertical menu sidebar inverted borderless thin ${props.toggle ? 'visible' : ''}`}>

            <div className={"menu-title"}>MENU</div>

            <Link to='/' className={"item link"}>
                <div className="centered menu-item">Overview</div>
            </Link>
            <Link to='/board' className={"item link"}>
                <div className="centered menu-item">Board</div>
            </Link>
            <Link to='/watch-list' className={"item link"}>
                <div className="centered menu-item">Watch List</div>
            </Link>
            <Link to='/insider-trading' className={"item link"}>
                <div className="centered menu-item">Insider Trading</div>
            </Link>


            <div className={"menu-title"}>SETTINGS</div>

            <Link to='/alert' className={"item link"}>
                <div className="centered menu-item">Alert</div>
            </Link>
        </div>

    )
} 