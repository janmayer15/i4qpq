import React, {useEffect, useRef} from "react";
import {useState} from "react";
import classNames from "classnames";
import {Button} from "primereact/button";
import {InputText} from "primereact/inputtext";
import {FileUpload} from "primereact/fileupload";
import {Toolbar} from "primereact/toolbar";
import {DataTable} from "primereact/datatable";
import {Column} from "primereact/column";
import {Dialog} from "primereact/dialog";
import {InputTextarea} from "primereact/inputtextarea";
import {Link} from "react-router-dom";
import {Toast} from "primereact/toast";
import {RadioButton} from "primereact/radiobutton";
import {nodeService} from "../service/NodeService";

const DataTable_component = (props) => {
    let emptyInstance = {
        id: '',
        name: '',
        startDate: '',
        endDate: '',
        status: '',
        description: '',
    };
    const [instance, setInstance] = useState(emptyInstance);
    const [instances, setInstances] = useState(null);
    const [submitted, setSubmitted] = useState(false);
    const [globalFilter, setGlobalFilter] = useState(null);
    const [instanceDialog, setInstanceDialog] = useState(false);
    const [instanceDelete, setInstanceDelete] = useState(null);
    const [deleteInstanceDialog, setDeleteInstanceDialog] = useState(false);
    const [selectedInstancesTable, setSelectedInstancesTable] = useState([]);
    const [deleteInstancesDialog, setDeleteInstancesDialog] = useState(false);
    const toast = useRef(null);
    const dt = useRef(null);

    useEffect(() => {
        nodeService.getInstances().then(data => setInstances(data));
    }, []);

    const editInstance = (element) => {
        //let value = element.id;
        setInstance(element);
        setInstanceDialog(true);
    }
    const confirmDeleteInstance = (element) => {
        setInstanceDelete(element);
        setDeleteInstanceDialog(true);
    }

    const actionBodyTemplate = (rowData) => {
        return (
            <React.Fragment>
                <Button icon="pi pi-pencil" className="p-button-raised p-button p-mr-2 pencil"
                        onClick={() => editInstance(rowData)}/>
                <Button icon="pi pi-trash" className="p-button-raised p-button-danger"
                        onClick={() => confirmDeleteInstance(rowData)}/>
            </React.Fragment>
        );
    }

    const statusBody = (rowData) => {
        const state = rowData.status.replace(" ", '');
        return (
            <div className={`status-${state}`}>
                <p className={`${state}`}>{rowData.status.toUpperCase()}</p>
            </div>
        );
    }

    const onInputChange = (e, name) => {
        const val = (e.target && e.target.value) || '';
        let _instance = {...instance};
        _instance[`${name}`] = val;

        setInstance(_instance);
    }

    const confirmDeleteSelected = () => {
        setDeleteInstancesDialog(true);
    }
    const hideDeleteInstancesDialog=()=>{
        setDeleteInstancesDialog(false);
    }
    const hideDeleteInstanceDialog=()=>{
        setDeleteInstanceDialog(false);
    }
    const deleteInstances = () => {
        let _instances = instances.filter(val => !selectedInstancesTable.includes(val));
        setInstances(_instances);
        setDeleteInstancesDialog(false);
        setSelectedInstancesTable(null);
        toast.current.show({ severity: 'success', summary: 'Successful', detail: 'Products Deleted', life: 3000 });
    }

     const deleteInstance = () => {
        let _instances = instances.filter(val => val.id !== instanceDelete.id);
        setInstances(_instances);
        setDeleteInstanceDialog(false);
        setInstanceDelete(emptyInstance);
        toast.current.show({ severity: 'success', summary: 'Successful', detail: 'Elements Deleted', life: 3000 });
     }

    const deleteInstanceDialogFooter = (
        <React.Fragment>
            <Button label="No" icon="pi pi-times" className="p-button-raised p-button-danger" onClick={hideDeleteInstanceDialog} />
            <Button label="Yes" icon="pi pi-check" className="p-button-raised p-button-success" onClick={deleteInstance}/>
        </React.Fragment>
    );

    const deleteInstancesDialogFooter = (
        <React.Fragment>
            <Button label="No" icon="pi pi-times" className="p-button-raised p-button-danger" onClick={hideDeleteInstancesDialog} />
            <Button label="Yes" icon="pi pi-check" className="p-button-raised p-button-success" onClick={deleteInstances}/>
        </React.Fragment>
    );

    const exportCSV = () => {
        dt.current.exportCSV();
    }
    const openNew = () => {
        let value = "new";
        //setSubmitted(false);
        return "/item:"+value;
    }

    const header = (
        <div className="table-header" style={{height:40}}>
            <Link to={openNew}><Button type="button" label={'add Task'} icon="pi pi-plus" className="p-button-raised p-mr-4"
                    style={{backgroundColor: '#56717d', borderColor: '#56717d', color: 'white'}}/></Link>
            <span className="p-input-icon-left" style={{float:'right', position: 'flex'}}>
                <i className="pi pi-search" style={{}}/>
                <InputText type="search" onInput={(e) => setGlobalFilter(e.target.value)} placeholder='Search' />
            </span>
        </div>
    );

    const hideEditInstanceDialog = () => {
        setInstanceDialog(false)
        setSubmitted(false);
    }

    const saveTask =() => {
        //let oldInstance = instances.filter(value => value.id === instance.id)
        let newInstances = instances
        let index = instances.findIndex(value => value.id === instance.id)
        if(index >= 0){
            newInstances[index] = instance
            console.log(newInstances)
        }
        setInstances(newInstances)
        setInstanceDialog(false)
    }

    const instanceDialogFooter = (
        <React.Fragment>
            <Button label="Save" icon="pi pi-check" className="p-button-success" onClick={saveTask} />
            <Button label="Cancel" icon="pi pi-times" className="p-button" onClick={hideEditInstanceDialog} />
        </React.Fragment>
    );

    const onCategoryChange = (e) => {
        let _instance = {...instance};
        _instance['status'] = (e.value);
        setInstance(_instance);
    }

    const buttons = (
        <React.Fragment>
            <div className="fc-button-group" style={{display: 'flex'}}>
                <Button label={'Export'} icon="pi pi-upload" className="p-button p-mr-2 export" onClick={exportCSV}/>
                <FileUpload mode="basic" accept="image/*" maxFileSize={1000000} label={'Import'} chooseLabel={'Import'} className="p-mr-2"/>
                <Button label={'Delete'} icon="pi pi-trash" className="p-button p-button-danger p-mr-2" onClick={confirmDeleteSelected} disabled={!selectedInstancesTable || !selectedInstancesTable.length} />
            </div>
        </React.Fragment>
    );

    return(
        <div>
            <div className="card" style={{paddingTop: 20}}>
                <Toast ref={toast} />
                <Toolbar className="p-mb-4" left={buttons}/>
                <div style={{marginTop: 15}}>
                    <DataTable ref={dt} value={instances} selection={selectedInstancesTable} onSelectionChange={(e) => setSelectedInstancesTable(e.value)}
                           dataKey="id" paginator rows={10} rowsPerPageOptions={[5, 10, 25]}
                           paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                           currentPageReportTemplate="Showing {first} to {last} of {totalRecords} elements"
                           globalFilter={globalFilter}
                           header={header}>
                        <Column selectionMode="multiple" headerStyle={{ width: '3rem' }}/>
                        <Column body={actionBodyTemplate} style={{width: '110px', padding: '5px', textAlign: 'center'}}/>
                        <Column header='id' field="id" headerStyle={{ width: '3rem' }}/>
                        <Column header='Name' field="name" sortable/>
                        <Column field="startDate" header={'Start Date'} sortable/>
                        <Column field="endDate" header={'End Date'} sortable/>
                        <Column field="status" body={statusBody} header={'Status'} sortable/>
                    </DataTable>
                </div>
            </div>

            <Dialog visible={instanceDialog} style={{ width: '600px' }} header="Tasks" footer={instanceDialogFooter} modal onHide={hideEditInstanceDialog}>
                <div className="p-fluid">
                    <div className="p-field ID">
                        <label htmlFor="id">ID: {instance.id}</label>
                    </div>
                    <div className="p-field inlineStyle">
                        <label htmlFor="name" style={{marginRight: 15}}>Name</label>
                        <InputText id="name" value={instance.name} onChange={(e) => onInputChange(e, 'name')}
                                       required autoFocus
                                       className={classNames({'p-invalid': submitted && !instance.name})}/>
                        {submitted && !instance.name && <small className="p-error">Name is required.</small>}
                    </div>
                    <div className="p-field inlineStyle">
                        <label htmlFor="startDate" style={{marginRight: 15}}>Start Date</label>
                        <InputText id="startDate" value={instance.startDate} onChange={(e) => onInputChange(e, 'startDate')}
                                   autoFocus className={classNames({'p-invalid': submitted && !instance.startDate})}/>
                                    {submitted && !instance.startDate && <small className="p-error">Start Date is required.</small>}
                    </div>
                    <div className="p-field inlineStyle">
                        <label htmlFor="endDate" style={{marginRight: 15}}>End Date</label>
                        <InputText id="endDate"
                                   value={instance.endDate} onChange={(e) => onInputChange(e, 'endDate')}
                                   autoFocus className={classNames({'p-invalid': submitted && !instance.endDate})}/>
                        {submitted && !instance.endDate && <small className="p-error">Start Date is required.</small>}
                    </div>
                    <div className="p-field">
                        <label className="p-mb-3" style={{marginRight: 15}} >Status</label>
                        <div className="" style={{display: 'inline-flex'}}>
                            <div className="p-field-radiobutton"style={{marginRight: 25}}>
                                <RadioButton inputId="new" name="status" value="new" onChange={onCategoryChange} checked={instance.status === 'new'} style={{marginRight: 5}}/>
                                <label htmlFor="new">New</label>
                            </div>
                            <div className="p-field-radiobutton" style={{marginRight: 25}}>
                                <RadioButton inputId="unqualified" name="status" value="qualified" onChange={onCategoryChange} checked={instance.status === 'qualified'} style={{marginRight: 5}}/>
                                <label htmlFor="qualified">Qualified</label>
                            </div>
                            <div className="p-field-radiobutton" style={{marginRight: 25}}>
                                <RadioButton inputId="unqualified" name="status" value="unqualified" onChange={onCategoryChange} checked={instance.status === 'unqualified'} style={{marginRight: 5}}/>
                                <label htmlFor="unqualified">Unqualified</label>
                            </div>
                        </div>
                    </div>
                    <div className="p-field" style={{marginTop: 15, marginBottom: 10}}>
                        <label htmlFor="description">Description</label>
                        <InputTextarea id="description" style={{marginTop: 10}}
                                   value={instance.description || ""} onChange={(e) => onInputChange(e, 'description')}
                                   autoFocus className={classNames({'p-invalid': submitted && !instance.description})}
                        />
                    </div>
                </div>
            </Dialog>
            <Dialog visible={deleteInstancesDialog} style={{ width: '480px' }} header="Confirm" modal footer={deleteInstancesDialogFooter} onHide={hideDeleteInstancesDialog}>
                <div className="confirmation-content">
                    <i className="pi pi-exclamation-triangle p-mr-3" style={{ fontSize: '2rem'}} />
                    {instance && <span>Are you sure you want to delete the selected elements?</span>}
                </div>
            </Dialog>
            <Dialog visible={deleteInstanceDialog} style={{ width: '480px' }} header="Confirm" modal footer={deleteInstanceDialogFooter} onHide={hideDeleteInstanceDialog}>
                <div className="confirmation-content">
                    <i className="pi pi-exclamation-triangle p-mr-3" style={{ fontSize: '2rem'}} />
                    {instance && <span>Are you sure you want to delete the selected element?</span>}
                </div>
            </Dialog>
        </div>
    );
}
export default DataTable_component;