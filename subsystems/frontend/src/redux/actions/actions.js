import { SEND_TAGS, READ_TAGS } from '../constants/types';

export const sendFlags = (flags) => dispatch => {
    // console.log('sending')
    dispatch({
        type: SEND_TAGS,
        payload: flags
    })
}

export const readFlags = () => dispatch => {
    // console.log('reading')
    dispatch({
        type: READ_TAGS
    })
}