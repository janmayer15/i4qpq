import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import logo from './i4Qlogo.png';

class AppTopbar extends React.Component{

    static defaultProps = {
        onToggleMenu: null
    }

    static propTypes = {
        onToggleMenu: PropTypes.func.isRequired
    }

    render(){
        return (
            <div className="layout-topbar clearfix">
                <button className="p-link layout-menu-button" onClick={this.props.onToggleMenu}>
                    <span className="pi pi-bars"/>
                </button>
                <Link to={'/'} style={{float:'right'}}>
                    <button className="p-link layout-menu-button" style={{padding:0}}>
                        {/* <span className="pi pi-home"/> */}
                        <img src={logo} style={{width: 30, display:'block'}}></img>
                    </button>
                </Link>
            </div>
        );
    }
}

export default AppTopbar;