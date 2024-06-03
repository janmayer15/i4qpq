import streamlit as st
from PIL import Image


def app():

    background = Image.open("img/i4Q.png")
 
    st.image(background, use_column_width=True)
    
    st.title('Continuous Process Qualification')

    st.markdown(
        'Welcome to the interface of the Continuous Process Qualification! '
        'With this software, it is possible to check your current process capability.'
        ' By adding the connection to your data source and choosing the variable you are interested in, '
        'you can check if the process will produce in your desired quality range.'
        )
    
    # import streamlit_scrollable_textbox as stx

    # long_text = "Input here"
    # stx.scrollableTextbox(long_text,height = 300)

    

