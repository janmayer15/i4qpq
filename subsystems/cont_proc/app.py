import streamlit as st
from multiapp import MultiApp
from apps import frontlayer, SecondLayer, ThirdLayer # import your app modules here

app = MultiApp()

# Add all your applications
app.add_app("Home", frontlayer.app)
app.add_app("Statistical Process Control", SecondLayer.app)
app.add_app("Continuous Process Qualification", ThirdLayer.app)

# main app
app.run()