import { createStore, applyMiddleware } from "redux";
import thunk from 'redux-thunk'
import rootReducer from '../redux/reducers/reducer';

const initialState = {};
const middleware = [thunk];

//store
let store = createStore(rootReducer,initialState, applyMiddleware(...middleware));

export  default store;