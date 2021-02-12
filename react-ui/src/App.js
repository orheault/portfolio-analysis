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
        <div style={{backgroundColor: "#2a3042"}}
             className={`ui left vertical menu sidebar inverted ${toggle ? 'visible' : ''}`}>
          {/*className={`ui sidebar inverted vertical menu ${toggleMenu ? 'visible' : ''}`}>*/}
          <Link to='/' className={"item link"}>
            <div className="centered">Home</div>
          </Link>
          <Link to='/404' className={"item link"}>
            <div className="centered">404</div>
          </Link>
        </div>

        <div className="ui top fixed menu">
          <div className="item" onClick={toggleMenu}>
            <Icon name='sidebar' size='large' className='link'/>
          </div>
          <SearchTicker className='item'/>
        </div>

        <div style={{marginTop: 65, height:'100%'}} className="pusher blend-white ">
          {/*<TopMenu onToggleMenu={toggleMenu}/>*/}
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
