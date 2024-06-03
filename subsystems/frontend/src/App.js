import React from 'react';
import store from "./helpers/store";
import classNames from "classnames";
import New from "./components/New";
import Detail from "./pages/Detail";
import Table from "./pages/Table";
import Icons from "./pages/Icons";
import Graphs from "./pages/Graphs";
import Help from "./pages/Help";
import { Home } from "./pages/Home";
import AppTopbar from "./components/AppTopbar";
import { Route } from "react-router-dom";
import { Provider } from "react-redux";
import { AppMenu } from "./components/AppMenu";
import { AppFooter } from "./components/AppFooter";
// Template de primereact. 
// import 'primereact/resources/themes/nova/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import '@material-ui/icons';
import 'primeflex/primeflex.css';
// Modificaciones sobre primereact.
import './theme/themes/nova/theme.css'
import './theme/themes/nova-light/theme.css';
import './App.css';
import './theme/layout/layout.scss'


class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      layoutMode: 'static',
      layoutColorMode: 'dark',
      menu: [
        { label: 'Home', icon: 'pi pi-fw pi-home', to: '/', badge: 0, notifications: false },
        { label: 'Help', icon: 'pi pi-fw pi-question', to: '/help', badge: 0, notifications: false },
        { label: 'Graphs', icon: 'pi pi-fw pi-chart-line', to: '/graphs', badge: 0, notifications: true },
        { label: 'Table', icon: 'pi pi-fw pi-table', to: '/table', badge: 0, notifications: false },
        { label: 'Icons', icon: 'pi pi-fw pi-file-o', to: '/icons', badge: 0, notifications: false }
      ],
      userLoggedIn: false,
      staticMenuInactive: false,
      overlayMenuActive: false,
      mobileMenuActive: false,

      //notifications: null
    };
    this.onWrapperClick = this.onWrapperClick.bind(this);
    this.onToggleMenu = this.onToggleMenu.bind(this);
    this.onSidebarClick = this.onSidebarClick.bind(this);
    this.onMenuItemClick = this.onMenuItemClick.bind(this);
    this.state.userLoggedIn = true
  }

  componentDidMount() {
  }

  onWrapperClick(event) {
    if (!this.menuClick) {
      this.setState({
        overlayMenuActive: false,
        mobileMenuActive: false
      });
    }
    this.menuClick = false;
  }

  onToggleMenu(event) {
    this.menuClick = true;
    if (this.isDesktop()) {
      if (this.state.layoutMode === 'overlay') {
        this.setState({
          overlayMenuActive: !this.state.overlayMenuActive
        });
      } else if (this.state.layoutMode === 'static') {
        this.setState({
          staticMenuInactive: !this.state.staticMenuInactive
        });
      }
    } else {
      const mobileMenuActive = this.state.mobileMenuActive;
      this.setState({
        mobileMenuActive: !mobileMenuActive
      });
    }
    event.preventDefault();
  }

  onSidebarClick(event) {
    this.menuClick = true;
  }

  onMenuItemClick(event) {
    if (!event.item.items) {
      this.setState({
        overlayMenuActive: false,
        mobileMenuActive: false
      })
    }
  }

  addClass(element, className) {
    if (element.classList)
      element.classList.add(className);
    else
      element.className += ' ' + className;
  }

  removeClass(element, className) {
    if (element.classList)
      element.classList.remove(className);
    else
      element.className = element.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
  }

  isDesktop() {
    // return window.innerWidth > 512;
    return window.innerWidth > 1024;
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (this.state.mobileMenuActive)
      this.addClass(document.body, 'body-overflow-hidden');
    else
      this.removeClass(document.body, 'body-overflow-hidden');
  }

  render() {
    const wrapperClass = classNames('layout-wrapper', {
      'layout-overlay': this.state.layoutMode === 'overlay',
      'layout-static': this.state.layoutMode === 'static',
      'layout-static-sidebar-inactive': this.state.staticMenuInactive && this.state.layoutMode === 'static',
      'layout-overlay-sidebar-active': this.state.overlayMenuActive && this.state.layoutMode === 'overlay',
      'layout-mobile-sidebar-active': this.state.mobileMenuActive
    });
    const portalWrapperClass = classNames('portal-wrapper');

    const sidebarClassName = classNames("layout-sidebar", {
      'layout-sidebar-dark': this.state.layoutColorMode === 'dark',
      'layout-sidebar-light': this.state.layoutColorMode === 'light'
    });

    return (
      <Provider store={store}>
        <div className={wrapperClass} onClick={this.onWrapperClick}>
          <div className={portalWrapperClass} />
          <AppTopbar onToggleMenu={this.onToggleMenu} />
          <div ref={(el) => this.sidebar = el} className={sidebarClassName} onClick={this.onSidebarClick}>
            <AppMenu model={this.state.menu} onMenuItemClick={this.onMenuItemClick} />
          </div>
          <div className="layout-main">
            <Route exact path="/">
              <Home/>
            </Route>
            <Route exact path="/help">
              <Help/>
            </Route>
            <Route exact path="/graphs">
              <Graphs />
            </Route>
            <Route exact path="/item:id">
              <New />
            </Route>
            <Route exact path="/detail">
              <Detail />
            </Route>
            <Route exact path="/table">
              <Table />
            </Route>
            <Route exact path="/icons">
              <Icons/>
            </Route>
          </div>
          <AppFooter />
        </div>
      </Provider>
    );
  }
}
export default App;
