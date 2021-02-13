import 'semantic-ui-css/semantic.min.css'
import './App.css';

import {BrowserRouter as Router, Link, Redirect, Route, Switch} from 'react-router-dom';

// Components
import {useState} from 'react';

// Pages
import {MainPage} from "./pages/index";
import {NotFoundPage} from './pages/404';
import {SideMenuVertical} from "./components/SideMenuVertical";
import {TopMenu} from "./components/TopMenu";

function App() {

  const [toggle, setToggle] = useState(true);

  function toggleMenu() {
    setToggle(!toggle);
  }

  return (
      <Router>
        <SideMenuVertical toggle={toggle} />
        <TopMenu toggle={toggleMenu}/>

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
