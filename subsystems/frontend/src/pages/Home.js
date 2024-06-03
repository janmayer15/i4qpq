import React from 'react';
import {Button} from "primereact/button";
import {Card} from "primereact/card";
import {Dialog} from "primereact/dialog";
import {Link} from "react-router-dom";

export class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            active: false
        }
    }

    componentDidMount() {
        console.log(this.state.userLoggedIn)
    }

    render() {

        const header1 = <i className="pi pi-briefcase" style={{'fontSize': '6em', paddingTop: 10, marginTop:15, color: '#8b569c'}}/>;
        const header2 = <i className="pi pi-star" style={{'fontSize': '6em', paddingTop: 10, marginTop:15, color: '#8b569c'}}/>;
        const header3 = <i className="pi pi-pencil" style={{'fontSize': '6em', paddingTop: 10, marginTop:15, color: '#8b569c'}}/>;
        const header4 = <i className="pi pi-clone" style={{'fontSize': '6em', paddingTop: 10, marginTop:15, color: '#8b569c'}}/>;

        return (
            <div className="p-list contentpage" style={{marginTop: 20, marginBottom: 15}}>
                <Card title="Welcome to the i4Q template" className="contentcard">
                    <div style={{lineHeight: 1.8, fontSize:18}}>
                        Lorem ipsum
                    </div>
                    <div style={{textAlign: 'right', marginBottom: 0}}>
                        <Button label="More info" icon="pi pi-plus" className="p-button-raised"/>
                    </div>
                </Card>

                <div className="cards_list" style={{'textAlign': 'center', marginTop: 10}}>
                    <div className="p-col">
                        <Link to={`/help`}>
                            <Card title="Create a Project" style={{height: '100%'}} header={header1}>
                                <div>Create a project from scratch</div>
                            </Card>
                        </Link>
                    </div>

                    <div className="p-col">
                        <Link to={`/table`}>
                            <Card title="View your Projects" style={{height: '100%'}} header={header2}>
                                <div>View the projects that you have created</div>
                            </Card>
                        </Link>
                    </div>
                    <div className="p-col">
                        <Link to={`/graphs`}>
                            <Card title="Register a Resource" style={{height: '100%'}} header={header3}>
                                <div>Register an Algorithm or Dataset</div>
                            </Card>
                        </Link>
                    </div>
                    <div className="p-col">
                        <Link to={`/icons`}>
                            <Card title="View your Resources" style={{height: '100%'}} header={header4}>
                                <div>View your resources</div>
                            </Card>
                        </Link>
                    </div>
                </div>

                <Dialog header="Readme Details" visible={this.state.visible2} style={{width: '80vw'}} modal={true}
                        onHide={() => this.setState({visible2: false})}>
                </Dialog>
            </div>
        );
    }
}