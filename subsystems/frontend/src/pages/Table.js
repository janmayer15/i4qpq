import React from "react";
import {useEffect, useState} from "react";
import DataTable_component from "../components/DataTable_component";
import {nodeService} from "../service/NodeService";
import {Typography} from "@material-ui/core";
import {Button} from "primereact/button";

const Table = () => {

    return (
        <div className="contentpage">
            <Typography variant="h5" gutterBottom style={{marginTop: '10px'}}>
                <div> DataTable example </div>
            </Typography>
            <div className="card contentcard">
                <div style={{fontSize:"15px"}}>
                    <p style={{marginBottom: "0px", paddingLeft: '15px', paddingRight: '5px'}}>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                </div>
                <DataTable_component/>
            </div>
        </div>
    );
}
export default Table;