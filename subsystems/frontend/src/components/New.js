import React, {useEffect, useState} from "react";
import classNames from 'classnames';
import {Button} from "primereact/button";
import {InputText} from "primereact/inputtext";
import {InputTextarea} from "primereact/inputtextarea";
import {Typography} from "@material-ui/core";
import {Link} from "react-router-dom";
// import {nodeService} from "../service/NodeService";
// import {useParams} from "react-router";

const New = (props) => {
    let emptyInstance = {
        value1: '',
        name: '',
        value2: '',
        description: ''
    };

    const [instance, setInstance] = useState(emptyInstance);
    const [submitted, setSubmitted] = useState(false);

    // We can use this code to get an specific element and edit it.
    /*const { id } = useParams();
    useEffect(() => {
        nodeService.getInstances(id).then(data => setInstance(data));
    });*/

    const onInputChange = (e, name) => {
        const val = (e.target && e.target.value) || '';
        let _instance = {...instance};
        _instance[`${name}`] = val;

        setInstance(_instance);
    }

    return (
        <div className="contentpage">
            <Typography variant="h5" gutterBottom style={{marginTop: '10px'}}>
                <div> New item </div>
            </Typography>
            <div className="card contentcard">
                <div className="formgroup-inline">
                    <label htmlFor="code" style={{width: '150px', fontSize:'15px', fontWeight:'bold'}}>Value1</label>
                    <InputText id="code" value={instance.code} onChange={(e) => onInputChange(e, 'code')} required
                               autoFocus className={classNames({'p-invalid': submitted && !instance.code})}/>
                    {submitted && !instance.code && <small className="p-invalid">Code is required.</small>}
                </div>

                <div className="formgroup-inline" style={{margin: '10px 0px 0px 0px'}}>
                    <label htmlFor="name" style={{width: '150px', fontSize:'15px', fontWeight:'bold'}} >Name</label>
                    <InputText id="name" value={instance.name} onChange={(e) => onInputChange(e, 'name')} required
                               autoFocus className={classNames({'p-invalid': submitted && !instance.name})}/>
                    {submitted && !instance.name && <small className="p-invalid">Name is required.</small>}
                </div>

                <div className="formgroup-inline" style={{margin: '10px 0px 0px 0px'}}>
                    <label htmlFor="value2" style={{width: '150px', fontSize:'15px', fontWeight:'bold', verticalAlign: "top"}} >Tipo</label>
                    <InputText id="value2" value={instance.value2} onChange={(e) => onInputChange(e, 'value2')} required
                               autoFocus className={classNames({'p-invalid': submitted && !instance.name})}/>
                    {submitted && !instance.name && <small className="p-invalid">Name is required.</small>}
                </div>
                <div className="formgroup-inline" style={{margin: '10px 0px 0px 0px'}}>
                    <label htmlFor="description" style={{width: '150px', fontSize:'15px', fontWeight:'bold', verticalAlign: "top", paddingTop: 10}}>Description</label>
                    <InputTextarea id="description" value={instance.description}
                               onChange={(e) => onInputChange(e, 'description')} required rows={3} cols={80} />
                </div>
                <div className="fc-button-group" style={{marginTop: 15}}>
                    <Button label="Create" icon="pi pi-plus" className="p-button-success p-mr-2" />
                    <Link to="/table">
                        <Button label="Cancel" icon="pi pi-times-circle" className="p-button-danger p-mr-2"/>
                    </Link>
                </div>
            </div>
        </div>
    );
}
export default New;