import React from "react";
import {Typography} from "@material-ui/core";
// import BarChart from "../components/Charts/BarChart";
import ComboChart from "../components/Charts/BarChart";


const Graphs = () => {
    return (
        <div className="contentpage">
            <Typography variant="h5" gutterBottom style={{marginTop: '10px'}}>
                <div> Graph example </div>
            </Typography>
            <div className="card contentcard">
                <ComboChart/>
            </div>
        </div>
    );
}
export default Graphs;