#Import libraries

import streamlit as st
import numpy as np
import pandas as pd
import time
import statistics as stats
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from matplotlib.ticker import StrMethodFormatter
from pymongo import MongoClient
import pymongo
import pymysql



def app(): 
    # Set the Title for the App
    st.title('i4Q Continuous Process Qualification')

    ######################################################################################################################
                                    ################# SIDEBAR DATA CONNECTION #######################
    ######################################################################################################################


    # Sidebar purpose description
    # st.sidebar.write("Please enter your data connection:")    

    # # First Checkbox for data connector
    # if st.sidebar.checkbox("MongoDB"):

    #     # Create Variables for inserting them in url
    #     MDB_username = st.sidebar.text_input('Username')
    #     MDB_password = st.sidebar.text_input('Password')
    #     MDB_clustername = st.sidebar.text_input('Cluster Name')
    #     MDB_dbname = st.sidebar.text_input('DB Name')

    #     def get_database():
                
    #         # Provide the mongodb atlas url to connect python to mongodb using pymongo
    #         CONNECTION_STRING = "mongodb+srv://{}:{}@{}.mongodb.net/{}".format(MDB_username, MDB_password, MDB_clustername, MDB_dbname)

    #         # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    #         client = MongoClient(CONNECTION_STRING)

    #         # Create the database for our example (we will use the same database throughout the tutorial
    #         return client["data"]


    # if st.sidebar.checkbox("HTTP"):

    #     # Create Variables for inserting them in url
    #     HTTP_URL = st.sidebar.text_input('URL')
        
    # #### HERE MUST BE THE URL CONNECTION #####
    # if st.sidebar.checkbox("MySQL"):

    #     # Create Variables for inserting them in url
    #     MySQL_hostname = st.sidebar.text_input('Hostname')
    #     MySQL_password = st.sidebar.text_input('Password')
    #     MySQL_username = st.sidebar.text_input('Username')
    #     MySQL_dbname = st.sidebar.text_input('DB Name')

    #     myConnection = pymysql.connect(host=MySQL_hostname, user=MySQL_username, passwd=MySQL_password, db=MySQL_dbname)

    # response = st.text_input('Please enter your variable of interest:')