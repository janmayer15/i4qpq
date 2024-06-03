import React from "react";
import {Typography} from "@material-ui/core";
import {Card} from "primereact/card";

const Icons = () => {
    return (
        <div className="contentpage">
            <Typography variant="h5" gutterBottom style={{marginTop: '10px'}}>
                <div> ICONS </div>
            </Typography>
            <div className="card contentcard">
                <div className="cards_list">
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-search"/>
                        <b> pi-search </b>
                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-images"/>
                        <b> pi-images </b>

                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-slack"/>
                        <b> pi-slack </b>
                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-pencil"/>
                        <b> pi-pencil </b>
                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-times-circle"/>
                        <b> pi-times-circle </b>
                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-check"/>
                        <b> pi-check </b>
                    </Card>
                    <Card style={{margin: '15px'}}>
                        <i className="pi pi-ellipsis-v"/>
                        <b> pi-ellipsis-v </b>
                    </Card>
                </div>
            </div>
        </div>
    );
}
export default Icons;