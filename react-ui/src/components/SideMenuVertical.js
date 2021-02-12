import { Link } from 'react-router-dom';

export const SideMenuVertical = (props) => {

    return (
        <div style={{backgroundColor :"#2a3042"}} className={`ui menu sidebar left vertical pointing ${props.toggleMenu ? 'visible' : ''}`}>
            <Link to='/'><div className="item link">Home</div></Link>
            <Link to='/404'><div className="item link">404</div></Link>
        </div>
    )
} 