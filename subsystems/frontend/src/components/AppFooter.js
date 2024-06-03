import React, {Component} from "react";
import {Link, Typography} from "@material-ui/core";

export class AppFooter extends Component {
    render(){
        return(
            // <div className="alwaysDown">
                <div className="layout-footer">
                    <Typography variant="body2" color="textSecondary" align="center">
                        {'Copyright © '}
                        <Link color="inherit" href="https://www.cigip.upv.es/">
                            CIGIP
                        </Link>{' '}
                        {(new Date().getFullYear())}
                        {'.'}
                    </Typography>
                </div>
            // </div>
        );
    }
}