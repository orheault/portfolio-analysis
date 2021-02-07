import 'semantic-ui-css/semantic.min.css'
import './App.css';

import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

// Components
import { SideMenuVertical } from './components/SideMenuVertical'
import { TopMenu } from './components/TopMenu';
import { useState } from 'react';

// Pages
import { MainPage } from "./pages/index";
import { NotFoundPage } from './pages/404';

function App() {

  const [toggle, setToggle] = useState(false);

  function toggleMenu() {
    setToggle(!toggle);
  }

  return (
    <div>
      <TopMenu onToggleMenu={toggleMenu} />
      <div className="ui attached pushable"
        style={{ height: '100vh' }}>
        <Router>
          <SideMenuVertical toggleMenu={toggle} />
          <div className="pusher bottom">

            <Switch>
              <Route exact path="/" component={MainPage} />
              <Route exact path="/404" component={NotFoundPage} />
              <Redirect to="/404" />
            </Switch>
          </div>
        </Router>
      </div>
    </div >
  );
}

export default App;
