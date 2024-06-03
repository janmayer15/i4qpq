import React from 'react';
import { Link } from "react-router-dom";
import { Typography } from "@material-ui/core";



const Help = () => {
    return (
        <div className="contentpage">
            <Typography variant="h4" style={{ margin: '20px 0px' }} gutterBottom>
                <div>I4Q - Industrial Data Services for Quality Control in Smart Manufacturing</div>
            </Typography>
            <div className="card contentcard">
                <div style={{marginBottom: '15px'}}>
                    <Typography>
                        They adapt their process to produce goods adapted to specific requirements and produced under the minimum required production rate, guaranteeing high quality and limiting the use of resources in order to:
                        Are continuously facing the challenge of redesigning and adjusting their manufacture systems.
                    </Typography>
                </div>
                <Link to="/detail">
                    <b style={{fontSize: 20}}>Link to details</b>
                </Link>
            </div>
        </div>
    );
}
export default Help;