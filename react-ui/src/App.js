import 'semantic-ui-css/semantic.min.css'
import './App.css';

import {BrowserRouter as Router, Link, Redirect, Route, Switch} from 'react-router-dom';

// Components
import {useState} from 'react';

// Pages
import {MainPage} from "./pages/index";
import {NotFoundPage} from './pages/404';
import {Icon} from "semantic-ui-react";
import {SearchTicker} from "./components/SearchTicker";

function App() {

  const [toggle, setToggle] = useState(true);

  function toggleMenu() {
    setToggle(!toggle);
  }

  return (
      <Router>
        <div style={{backgroundColor: "#2a3042", paddingTop: 65}}
             className={`ui left vertical menu sidebar inverted borderless thin ${toggle ? 'visible' : ''}`}>

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

        <div className="ui top fixed menu borderless">
          <div className="item" onClick={toggleMenu}>
            <Icon name='sidebar' size='large' className='link'/>
          </div>
          <SearchTicker className='item'/>
        </div>

        <div style={{paddingTop: 65, height:'100%'}} className="pusher blend-white ">
          <Switch>
            <Route exact path="/" component={MainPage}/>
            <Route exact path="/404" component={NotFoundPage}/>
            <Redirect to="/404"/>
          </Switch>
        </div>

      </Router>
  )
}

export default App;
