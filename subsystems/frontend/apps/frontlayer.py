import streamlit as st

def app():
    st.title('i4Q Continuous Process Qualification')

    st.markdown(
        'Welcome to the interface of the Continuous Process Qualification!'
        'With this software, it is possible to check your current process capability.'
        'By adding the connection to your data source and choosing the variable you are interested in, '
        'you can check if the process will produce in your desired quality range.'
        )

    st.write('Please anser the follwing question:')

    progress = st.radio(
        "Do you want to use static or dynamic data?",
        ('Static', 'Dynamic'))