import { Container, Icon, Menu, Sidebar } from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css'
import './App.css';

import { SideMenuVertical } from './components/SideMenuVertical'
import { TopMenu } from './components/TopMenu';
import { Main } from "./components/Main";
import { useState } from 'react';

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
        <SideMenuVertical toggleMenu={toggle} />
        <div className="pusher bottom">
          <Main />
        </div>
      </div>
    </div>
  );
}

export default App;
