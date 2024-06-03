import { SEND_TAGS, READ_TAGS } from '../constants/types';

const initialState = {
    flags: []
}

export default function reducer(state = initialState, action){
    switch (action.type){
        case SEND_TAGS:
            return {
                ...state,
                flags: action.payload
            }
        case READ_TAGS:
            return state
        default:
            return state;
    }
}