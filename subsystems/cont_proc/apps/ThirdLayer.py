import datetime
import json
import logging
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
# import utilities
# from message_broker import Consumer
import confluent_kafka

# from ksql import KSQLAPI

logging.raiseExceptions = False

import time
from collections import deque
from datetime import datetime


from confluent_kafka import Consumer, KafkaException
import json
import pandas as pd
import uuid
# from message_broker import Consumer

import plotly.graph_objects as go

def create_consumer(server, group_id=None):
    """Create a Kafka consumer."""
    if group_id is None:
        group_id = str(uuid.uuid4())  # Generate a unique group ID

    conf = {
        'bootstrap.servers': server,
        'group.id': group_id,
        'auto.offset.reset': 'latest', 
        
        'security.protocol': 'SSL',
        # Specify SSL configurations here, for example:
        'security.protocol': 'SSL',
        'ssl.ca.location': './Certificates/client/CARoot.pem',
        'ssl.key.location': './Certificates/client/key.pem',
        'ssl.certificate.location': './Certificates/client/certificate.pem'

    }


    return Consumer(conf)

def read_latest_message(consumer, topic):
    """Read the latest message from the specified Kafka topic."""
    consumer.subscribe([topic])

    try:
        msg = consumer.poll(timeout=10.0)
        if msg is None:
            return None
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                print('%% %s [%d] reached end at offset %d\n' %
                      (msg.topic(), msg.partition(), msg.offset()))
            else:
                raise KafkaException(msg.error())
        else:
            # Proper message
            record = json.loads(msg.value().decode('utf-8'))
            df = pd.DataFrame([record])
            return df
    finally:
        # Do not close the consumer here; it should be reused
        pass


def app(): 
    #Set the Title for the App
    st.title('i4Q Continuous Process Qualification')

    ######################################################################################################################
                                    ################# SIDEBAR DATA CONNECTION #######################
    ######################################################################################################################
    
    # Insert UCL and LCL
    st.sidebar.write("Please insert your Tolerance Levels:")

    UTL = st.sidebar.number_input('Upper Tolerance Level') 
    LTL = st.sidebar.number_input('Lower Tolerance Level')

    # Sidebar purpose description
    st.sidebar.write("Please enter your Kafka details:")

    # Enter the variable of interest
    Interest_var_kafka = st.sidebar.text_input("Please enter the variable you would like to evaluate:")    

    # # First text box for kafka topic
    # kafka_stream = st.sidebar.text_input("Kafka Stream:")

    # # Second text box for ksql server
    # ksql_server = st.sidebar.text_input("KSQL Server (Port Number):")

    # st.write('Kafka Host IP')
    # host_ip = st.sidebar.text_input('Kafka Host IP', value='10.1.10.41')
    host_ip = st.sidebar.text_input('Kafka Host IP', value='localhost:9092')


    # Insert topic.
    # st.write('Kafka Topic')
    # topic = st.sidebar.text_input('Kafka Topic', value='SensorsTopic')
    topic = st.sidebar.text_input('Kafka Topic', value='test')

    # First text box for kafka offset
    col1, col2 = st.columns(2)

    with col1:
        window_limit_low = LTL*0.75

    with col2:
        window_limit_up = UTL*1.25

    window_size = st.slider('Please select length of the window to display:', 1, 130, 20)
    
    # Kafka Consumer Configuration
    consumer = create_consumer(host_ip, group_id=None)

    if st.checkbox("Start Continuous Process Qualification!"):
        
        # Plotly figure setup
        fig = go.Figure()
        fig.update_layout(title='Process Control Chart', xaxis_title='Values', yaxis_title='Chosen Variable')
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Chosen Variable'))
        
        # Control limit lines
        UCL = UTL
        LCL = LTL
        fig.add_hline(y=UCL, line=dict(color='grey', dash='dash'), annotation_text=f"UTL = {UCL:.2f}")
        fig.add_hline(y=LCL, line=dict(color='grey', dash='dash'), annotation_text=f"LTL = {LCL:.2f}")

        fig.update_yaxes(range=[window_limit_low, window_limit_up])

        y = deque(np.zeros(window_size), maxlen=window_size)
        pq_list = deque(maxlen=130)
        cont_pq_history = deque(maxlen=1000000)  # Store history of cont_pq messages

        the_plot = st.plotly_chart(fig, use_container_width=True)

        def cpk_value(x):
            d={}
            cpk=abs(np.min([(UCL-np.mean(x))/(3*np.std(x)),(np.mean(x)-LCL)/(3*np.std(x))]))
            d['Process Mean:']=np.mean(x)
            d['Process Standard Deviation:']=np.std(x)
            d['Cpk Value:']=cpk
            return pd.Series(d, index=['Process Mean:', 'Process Standard Deviation:', 'Cpk Value:'])

        def animate():
            # Fetch the latest message
            latest_data = read_latest_message(consumer, topic)
            if latest_data is not None and Interest_var_kafka in latest_data.columns:
                new_value = latest_data[Interest_var_kafka].iloc[0]
                y.append(new_value)
                fig.data[0].x = list(range(len(y)))
                fig.data[0].y = list(y)

                # Correct way to change the line color to purple
                fig.data[0].line.color = 'purple'

                the_plot.plotly_chart(fig, use_container_width=True)

        def cont_pq():
            latest_message = read_latest_message(consumer, topic)
            if latest_message is not None and Interest_var_kafka in latest_message.columns:
                value = latest_message[Interest_var_kafka].iloc[0]
                pq_list.append(value)
                if len(pq_list) % 10 == 0:  # Calculate Cpk value every 10 messages
                    valid_values = [l for l in pq_list if l != 0]
                    if len(valid_values) >= 10:
                        Cp_norm = round(cpk_value(valid_values)[[2]], 4).iloc[0]
                        return Cp_norm, len(valid_values)
            return None, None

        # Create an empty container for current cpk value message
        current_cpk_container = st.empty()
        history_cpk_container = st.expander("Historical Process Qualification:", expanded=False)

        while True:
            animate()
            Cp_norm, count = cont_pq()
            if Cp_norm is not None:
                timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"{timenow}: Cpk-value is {Cp_norm} based on last {count} products."

                # Clear the current container before displaying the new message
                current_cpk_container.empty()

                # Update the container with the new message and add it to the history
                if Cp_norm < 1:
                    current_cpk_container.error(f"Watch out! Your current Cpk-value is: {Cp_norm}. Currently, your process is not qualified. Please note: This is an estimation based on the last {count} Products at {timenow}.")
                elif 1 <= Cp_norm <= 1.33:
                    current_cpk_container.warning(f"Be careful. Your current Cpk-value is: {Cp_norm}. Currently, your process is qualified but not in an ideal state. Please note: This is an estimation based on the last {count} Products at {timenow}.")
                else:
                    current_cpk_container.success(f"Awesome! Your current Cpk-value is: {Cp_norm}. Currently, your process is qualified. Please note: This is an estimation based on the last {count} Products at {timenow}.")

                # Append the message to history and display only the latest message in the history container
                if not cont_pq_history or cont_pq_history[0] != message:
                    cont_pq_history.appendleft(message)
                    with history_cpk_container:
                        st.write(cont_pq_history[0])
            time.sleep(0.01)








    # if st.checkbox("Start Continuous Process Qualification!"):


    #     fig, ax = plt.subplots()

    #     # create line plot for dependent variable which has to be visualized (20 is the default for the plotted values)
    #     ax.plot([0]*20, label='Chosen Variable', color='purple')
    #     ax.set_title('Process Control Chart', color='#8064a2')

    #     # create legend with default tick numbering and name it "values"
    #     ax.legend()
    #     ax.set_xlabel('values')

    #     # create grid background for better reading
    #     ax.grid()
                
    #     # create the Upper Control Limit Line
    #     UCL = UTL
    #     ax.axhline(UCL, color='grey')

    #     # create the Lower Control Limit Line
    #     LCL = LTL
    #     ax.axhline(LCL, color='grey')

    #     # create formatted values to display in the plot
    #     ax.text(1.07*window_size, UCL, "UTL = " + str("{:.2f}".format(UCL)), color='grey')
    #     ax.text(1.07*window_size, LCL, "LTL = " + str("{:.2f}".format(LCL)), color='grey')

    #     max_samples = window_size
    #     max_x = window_size
    #     max_rand = window_size

    #     x = np.arange(0, max_x)
    #     y = deque(np.zeros(max_samples), max_samples)
    #     pq_list = deque(np.zeros(130), 130)
    #     count_list = deque(np.zeros(1000000), 1000000)

    #     ax.set_ylim(window_limit_low, window_limit_up)
    #     line, = ax.plot(x, np.array(y))
    #     the_plot = st.pyplot(plt)

    #     def count_prod():
    #         with st.empty():
    #             for observations in range(0,1000000, 1):
    #                 count_list.append(np.array(read_latest_message()["RESPONSE"][[0]]))
    #                 st.info(f'Currently, {int(observations)} products have been evaluated.')
    #                 time.sleep(0.01)
    #             st.write("✔️ 1'000'000 products have been evaluated! Please start over again.")

    #     def animate():  # update the y values 
    #         latest_data = read_latest_message(consumer, topic)
    #         if latest_data is not None and Interest_var_kafka in latest_data.columns:
    #             new_value = latest_data[Interest_var_kafka].iloc[0]
    #             y.append(new_value)
    #         line.set_ydata(np.array(y))
    #         line.set_color("purple")
    #         the_plot.pyplot(plt)

    #     # def animate():  # update the y values 
    #     #     line.set_ydata(np.array(y))
    #     #     line.set_color("purple")
    #     #     the_plot.pyplot(plt)
    #     #     y.append(np.array(read_latest_message()[Interest_var_kafka][[0]])) 

    #     def cpk_value(x):
    #         d={}
    #         cpk=abs(np.mean([(UCL-np.mean(x))/(3*np.std(x)),(np.mean(x)-LCL)/(3*np.std(x))]))
    #         d['Process Mean:']=np.mean(x)
    #         d['Process Standard Deviation:']=np.std(x)
    #         d['Cpk Value:']=cpk
    #         return pd.Series(d, index=['Process Mean:', 'Process Standard Deviation:', 'Cpk Value:'])


    #     def cont_pq():
    #         # Fetch the latest message
    #         latest_message = read_latest_message(consumer, topic)
            
    #         if latest_message is not None and Interest_var_kafka in latest_message.columns:
    #             # Extract the single value and append to pq_list
    #             value = latest_message[Interest_var_kafka].iloc[0]
    #             pq_list.append(value)
    #         else:
    #             # Handle the case where no message is received or the column is missing
    #             pq_list.append(0)  # Or handle this scenario as per your application's logic

    #         if np.count_nonzero(pq_list) in range(10, 130, 10):
    #             list = []
    #             timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
    #             for l in pq_list:
    #                 if l != 0:  # Assuming 0 indicates no data or an error state
    #                     list.append(l)
                
    #             Cp_norm = round(cpk_value(list)[[2]], 4)
    #             Cp_norm = Cp_norm.iloc[0]

    #             if Cp_norm < 1:
    #                 st.error(f"Watch out! Your current Cpk-value is: {Cp_norm}. Currently, your process is not qualified. Please note: This is an estimation based on the last {np.count_nonzero(pq_list)} Products at {timenow}.")
    #             elif 1 <= Cp_norm <= 1.33:
    #                 st.warning(f"Be careful. Your current Cpk-value is: {Cp_norm}. Currently, your process is qualified but not in an ideal state. Please note: This is an estimation based on the last {np.count_nonzero(pq_list)} Products at {timenow}.")
    #             else:
    #                 st.success(f"Awesome! Your current Cpk-value is: {Cp_norm}. Currently, your process is qualified. Please note: This is an estimation based on the last {np.count_nonzero(pq_list)} Products at {timenow}.")

    #     while True:
    #         animate()
    #         # count_prod()
    #         with st.expander("Check Process Qualification:"):
    #             cont_pq()
    #         time.sleep(0.01)




