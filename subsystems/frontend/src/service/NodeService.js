export const nodeService ={
    getInstances,
    getInstanceId,
    getInstancesProcessed
}

function getInstances(){
    // let allInstances = instances.filter(item => item.id !=='new');
    return new Promise((resolve, reject) =>{
        resolve(instances);
    });
    
}

function getInstanceId(id){
    let instance = instances.filter(item => item.id === id);
    return new Promise((resolve, reject) =>{
        resolve(instance);
    });
}

function getInstancesProcessed(value){
    let count =  (instances.filter(item => item.processed === value)).length;
    return new Promise((resolve, reject) =>{
        resolve(count);
    });
}

const instances =[
    {
        id:'1', name: 'Joan F.', startDate: '23-10-2020', endDate: '13-02-2021', status: 'qualified', description:''
    },
    {
        id:'2', name: 'Mark L.', startDate: '23-4-2020', endDate: '15-10-2021', status: 'new', description:''
    },
    {
        id:'3', name: 'Lucy G.', startDate: '15-6-2020', endDate: '13-11-2021', status: 'qualified', description:''
    },
    {
        id:'4', name: 'Emmanuel X.', startDate: '23-12-2020', endDate: '21-05-2021', status: 'unqualified', description:''
    },
    {
        id:'5', name: 'Jean G.', startDate: '2-10-2020', endDate: '03-03-2021', status: 'new', description:''
    },
    {
        id:'6', name: 'Asiya M.', startDate: '19-7-2020', endDate: '18-02-2021', status: 'new', description:''
    },
    {
        id:'7', name: 'Joan', startDate: '23-10-2020', endDate: '13-02-2021', status: 'unqualified', description:''
    },
    {
        id:'8', name: 'Joan', startDate: '23-10-2020', endDate: '13-02-2021', status: 'unqualified', description:''
    }
]

