import logging
logging.raiseExceptions = False

# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
import datetime
import seaborn as sns
from fitter import Fitter
import scipy.stats as stats
from scipy.stats import weibull_min, uniform, gamma, rayleigh, norm
import warnings
warnings.filterwarnings("ignore")

import plotly.graph_objs as go
import plotly.figure_factory as ff

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Other imports remain the same

# Function to create and train Random Forest model
def train_random_forest(data, target, n_estimators=100):
    model = RandomForestRegressor(n_estimators=n_estimators)
    model.fit(data, target)
    return model

def calculate_dppm_for_distribution(dist, sample, LTL, UTL):
    if dist in ['uniform', 'gamma', 'rayleigh', 'weibull_min']:
        dppm = sample[(LTL < sample) & (sample < UTL)].size
    elif dist == 'norm':
        dppm = 1000000 - sample[(LTL < sample) & (sample < UTL)].size
    return dppm

# Define the best_fit_distribution function
def best_fit_distribution(data):
    distributions = ['uniform', 'norm', 'gamma', 'rayleigh', 'weibull_min']
    min_error = float('inf')
    best_distribution = None
    best_fit_params = None

    for distribution in distributions:
        if distribution == 'uniform':
            params = stats.uniform.fit(data)
            sample = stats.uniform.rvs(*params, size=1000000)
        elif distribution == 'norm':
            params = stats.norm.fit(data)
            sample = stats.norm.rvs(*params, size=1000000)
        elif distribution == 'gamma':
            params = stats.gamma.fit(data)
            sample = stats.gamma.rvs(*params, size=1000000)
        elif distribution == 'rayleigh':
            params = stats.rayleigh.fit(data)
            sample = stats.rayleigh.rvs(*params, size=1000000)
        elif distribution == 'weibull_min':
            params = stats.weibull_min.fit(data)
            sample = stats.weibull_min.rvs(*params, size=1000000)

        residuals = data - sample[:len(data)]
        sum_of_squares = np.sum(np.square(residuals))

        if sum_of_squares < min_error:
            min_error = sum_of_squares
            best_distribution = distribution
            best_fit_params = params

    return best_distribution, best_fit_params


def calculate_cpk(data, lsl, usl):
    """
    Calculate an analogous Cpk value for various distributions.

    :param data: Array of data points
    :param lsl: Lower Specification Limit
    :param usl: Upper Specification Limit
    :return: Cpk value
    """
    distribution = best_fit_distribution(data)[0]
    params = best_fit_distribution(data)[1]

    if distribution == 'norm':
        mean, std_dev = params
        cpk = min((usl - mean) / (3 * std_dev), (mean - lsl) / (3 * std_dev))
    elif distribution == 'uniform':
        min_val, max_val = params
        range_val = max_val - min_val
        cpk = min((usl - max_val) / (3 * range_val), (min_val - lsl) / (3 * range_val))
    elif distribution in ['gamma', 'rayleigh', 'weibull_min']:
        median = np.median(data)
        std_dev = np.std(data)
        cpk = min((usl - median) / (3 * std_dev), (median - lsl) / (3 * std_dev))
    else:
        raise ValueError("Unsupported distribution type")

    return cpk

def calculate_dppm(data, lsl, usl):
    """
    Calculate the Defective Parts Per Million (DPPM).

    :param data: Array of data points
    :param lsl: Lower Specification Limit
    :param usl: Upper Specification Limit
    :return: DPPM value
    """
    # Count how many data points fall outside the specification limits
    out_of_spec = np.sum((data < lsl) | (data > usl))

    # Calculate the percentage of out-of-spec data points
    out_of_spec_percentage = out_of_spec / len(data)

    # Scale the percentage to DPPM
    dppm = out_of_spec_percentage * 1000000 

    return dppm


def calculate_dppm1(distribution, cpk, *params):
    """
    Calculate the Defective Parts Per Million (DPPM) for various distributions.

    :param distribution: Distribution type (e.g., 'norm', 'weibull_min', 'uniform', 'gamma', 'rayleigh')
    :param cpk: The Cpk value
    :param params: Parameters of the distribution (shape, scale, location, etc.)
    :return: The DPPM value
    """
    if distribution == 'norm':
        # Normal distribution
        tail_area = stats.norm.cdf(-cpk, *params)
    elif distribution == 'weibull_min':
        # Weibull minimum distribution
        scale, loc = params
        tail_area = stats.weibull_min.cdf(loc - cpk * scale, *params)
    elif distribution == 'uniform':
        # Uniform distribution
        min_val, max_val = params
        tail_area = (min_val + cpk) / (max_val - min_val)
    elif distribution == 'gamma':
        # Gamma distribution
        tail_area = stats.gamma.cdf(-cpk, *params)
    elif distribution == 'rayleigh':
        # Rayleigh distribution
        tail_area = stats.rayleigh.cdf(-cpk, *params)
    else:
        raise ValueError("Unsupported distribution type")

    # Multiply by 2 for both tails (if applicable) and convert to parts per million
    dppm = tail_area * 2 * 1000000
    return dppm


def detect_trend(data):
    """
    Detects a trend in the given data array using linear regression.

    :param data: Array of data points
    :return: Tuple containing slope, intercept, and a boolean indicating if a significant trend is detected
    """
    # Generate an array representing time indices
    time_indices = np.arange(len(data))

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_indices, data)

    # Check if the slope is significantly different from zero
    trend_detected = p_value < 0.05  # Common threshold for statistical significance

    return slope, intercept, trend_detected


# Function to create histogram with CDF
def plot_histogram_with_cdf(response, LTL, UTL, process_mean, best_dist):
    # Ensure at least 5 bins
    nbins = max(5, int(np.sqrt(len(response))))

    # Calculate the bin width based on the desired number of bins
    bin_width = (max(response) - min(response)) / nbins

    hist_data = [response]
    group_labels = [best_dist]

    # Create the distribution plot with the calculated bin width
    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_width, show_hist=True, show_rug=False)
    
    # Add vertical lines for LTL, UTL, and Process Mean
    fig.add_trace(go.Scatter(x=[LTL, LTL], y=[0, 1], mode="lines", name="LTL", line=dict(color="red", dash="dash")))
    fig.add_trace(go.Scatter(x=[UTL, UTL], y=[0, 1], mode="lines", name="UTL", line=dict(color="red", dash="dash")))
    fig.add_trace(go.Scatter(x=[process_mean, process_mean], y=[0, 1], mode="lines", name="Process Mean", line=dict(color="purple", dash="dot")))

    fig.update_layout(xaxis_title="Data", yaxis_title="Density")
    return fig



def plot_process_control_chart(response, predictions, UTL, LTL):
    fig = go.Figure()

    # Combine actual values and predictions for a continuous line
    combined_y = np.concatenate([response, predictions])
    combined_x = np.arange(len(combined_y))

    # Plot actual values and predictions
    fig.add_trace(go.Scatter(x=combined_x[:len(response)], y=combined_y[:len(response)], mode='lines', name='Actual values', line=dict(color='grey')))
    fig.add_trace(go.Scatter(x=combined_x[len(response)-1:], y=combined_y[len(response)-1:], mode='lines', name='Predicted', line=dict(color='purple')))

    # Add a vertical line at the start of the predictions
    fig.add_vline(x=len(response)-1, line_dash="solid", line_color="black")

    # Add UTL and LTL lines
    fig.add_hline(y=UTL, line_dash="dash", line_color="red", annotation_text="UTL")
    fig.add_hline(y=LTL, line_dash="dash", line_color="red", annotation_text="LTL")

    # Update layout
    fig.update_layout(xaxis_title="Time Index", yaxis_title="Evaluation Variable", showlegend=True)

    return fig



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
    st.sidebar.write("Please enter your data connection:")    

    # # First Checkbox for data connector
    if st.sidebar.checkbox("MongoDB"):

        # Create Variables for inserting them in url
        MDB_username = st.sidebar.text_input('Username')
        MDB_password = st.sidebar.text_input('Password', type='password')
        MDB_server = st.sidebar.text_input('Server Name')
        MDB_port = st.sidebar.text_input('Port Name')
        MDB_collname = st.sidebar.text_input('Collection Name')
        MDB_dbname = st.sidebar.text_input('DB Name')

        # Check if all necessary information is provided
        if MDB_username and MDB_password and MDB_collname and MDB_dbname and MDB_server and MDB_port:
            # All information provided, proceed with MongoDB connection
            CONNECTION_STRING = "mongodb://{}:{}@{}:{}/".format(MDB_username, MDB_password, MDB_server, MDB_port)

            myclient = pymongo.MongoClient(CONNECTION_STRING)
            mydb = myclient[MDB_dbname]
            mycol = mydb[MDB_collname]

            record = mycol.find({}).limit(200)

            # convert to pd df
            data =  pd.DataFrame(list(record))
            data = data.head(1000) 
                        
            # insert forecast length
            forecast_window = st.slider('Please enter your desired forecast length here:', min_value=1, max_value=20, value=5, step=1) 
            Interest_var = st.selectbox('Please enter the variable you would like to evaluate:', data.columns, 0)
            
            # Inside the checkbox block where forecasting is performed
            if st.checkbox("Create Process Qualification Information with the above selected criteria"):

                output_container = st.container()

                with output_container:
                    # Optionally, create a collapsible section
                    with st.expander("Process Distribution and Actual Process Qualification", expanded=False):

                        response = np.array(data[Interest_var])

                        # Ensure the data is a NumPy array of floats
                        response = np.asarray(response, dtype=np.float64)

                        # Remove NaN and infinite values
                        response = response[np.isfinite(response)]

                        # calcuate process stats
                        process_mean = response.mean()
                        process_std = response.std()
                        process_min = response.min()
                        process_max = response.max()
                        process_std = response.std()

                        # Prepare data for Random Forest
                        X_train = response[:-forecast_window].reshape(-1, 1)
                        y_train = response[forecast_window:].reshape(-1, 1)

                        # Train Random Forest model
                        rf_model = train_random_forest(X_train, y_train.ravel())

                        # Make predictions
                        X_test = response[-forecast_window:].reshape(-1, 1)
                        predictions = rf_model.predict(X_test)

                        ### CURRENT PROCESS CAPABILITY
                        Cp_norm = round(calculate_cpk(response, LTL, UTL), 4)

                        if Cp_norm < 1:
                            st.error("Watch out! Your current Cpk-value is: {}. Currently, your process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        elif 1 <= Cp_norm <= 1.33:
                            st.warning("Be careful. Your current Cpk-value is: {}. Currently, your process is qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        else:
                            st.success("Awesome! Your current Cpk-value is: {}. Currently, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))


                        best_dist, best_params = best_fit_distribution(response)
                        if best_dist == 'uniform':
                            sample = uniform.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'norm':
                            sample = norm.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'gamma':
                            sample = gamma.rvs(best_params[0], best_params[1], best_params[2], size=1000000)
                        elif best_dist == 'rayleigh':
                            sample = rayleigh.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'weibull_min':
                            sample = weibull_min.rvs(best_params[0], best_params[1], best_params[2], size=1000000)

                        dppm = round(calculate_dppm(response, LTL, UTL), 0)
                        st.write(f'The current amount of defective parts per million for {best_dist} distribution is {dppm}.')


                        # Display Histogram with CDF
                        st.header("Process Distribution Chart")
                        hist_fig = plot_histogram_with_cdf(response, LTL, UTL, process_mean, best_dist)
                        st.plotly_chart(hist_fig)

                        # Interpretation text
                        st.markdown("### How to interpret the Histogram")
                        st.markdown("""
                        - **Density Near Quality Thresholds (LTL and UTL)**: High density near these limits indicates many products are close to being out of specification.
                        - **Density Centered Around Process Mean**: Suggests that most products meet quality standards, and the process is stable.
                        - **Spread of the Density**: Wide spread indicates high variability, while a narrow spread suggests consistency.
                        - **Skewness or Asymmetry**: Skewness could indicate a systematic bias in the production process.
                        - **Multiple Peaks**: May suggest varying quality levels from different sub-processes or machines.
                        - **Continuous Improvement**: Regular analysis of density changes can help in identifying trends for process adjustments.
                        """)


                output_container2 = st.container()

                with output_container2:
                    # Optionally, create a collapsible section
                    with st.expander("Process Chart and Future Process Qualification", expanded=False):

                        
                        #### PREDICTIVE PROCESS CAPABILITY
                        prediction = np.append(response[-(130-forecast_window):], predictions)
                        process_mean_pred = np.mean(prediction)
                        process_std_pred = np.std(prediction)
                        process_min_pred = np.min(prediction)
                        process_max_pred = np.max(prediction)

                        Cp_pred = round(calculate_cpk(prediction, LTL, UTL), 4)

                        if Cp_pred < 1:
                            st.error("Watch out! Your future Cpk-value is: {}. There is a risk, your future process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        elif 1 <= Cp_pred <= 1.33:
                            st.warning("Be careful. Your future Cpk-value is: {}. It might be, your future process qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        else:
                            st.success("Awesome! Your future Cpk-value is: {}. In the future, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))

                        # Detect trend
                        slope, intercept, trend_detected = detect_trend(prediction)

                        # Interpret and display the trend
                        if trend_detected:
                            if slope > 0:
                                trend_description = "Positive (Increasing)"
                            elif slope < 0:
                                trend_description = "Negative (Decreasing)"
                            else:
                                trend_description = "Neutral"
                            
                            st.warning(f"Trend Detected: {trend_description} with slope of {round(slope, 4)}")
                        else:
                            st.warning("No significant Trend detected")
                        

                        ### FORECAST PLOT
                        # st.line_chart(obtained_forecast, "Forecast values")

                        # # #########################################Process Control Chart#############################################
                            # Display Process Control Chart
                        st.header("Process Control Chart")
                        control_chart_fig = plot_process_control_chart(response, predictions, UTL, LTL)
                        st.plotly_chart(control_chart_fig)

            else:
            # Show a warning if any of the information is missing
                st.warning("Please insert all necessary information: Username, Password, Collection Name, and DB Name.")





    if st.sidebar.checkbox("HTTP"):

        # Create Variables for inserting them in url
        HTTP_URL = st.sidebar.text_input('URL')

        if HTTP_URL is not None:

            # convert to pd df
            data = pd.read_csv(HTTP_URL,sep=",", nrows=100) 

            # convert to pd df
            data = data.head(1000) 

            # insert forecast length
            forecast_window = st.slider('Please enter your desired forecast length here:', min_value=1, max_value=20, value=5, step=1) 
            Interest_var = st.selectbox('Please enter the variable you would like to evaluate:', data.columns, 0)

            if st.checkbox("Create Process Qualification Information with the above selected criteria"):

                output_container = st.container()

                with output_container:
                    # Optionally, create a collapsible section
                    with st.expander("Process Distribution and Actual Process Qualification", expanded=False):

                        response = np.array(data[Interest_var])

                        # Ensure the data is a NumPy array of floats
                        response = np.asarray(response, dtype=np.float64)

                        # Remove NaN and infinite values
                        response = response[np.isfinite(response)]

                        # calcuate process stats
                        process_mean = response.mean()
                        process_std = response.std()
                        process_min = response.min()
                        process_max = response.max()
                        process_std = response.std()

                        # Prepare data for Random Forest
                        X_train = response[:-forecast_window].reshape(-1, 1)
                        y_train = response[forecast_window:].reshape(-1, 1)

                        # Train Random Forest model
                        rf_model = train_random_forest(X_train, y_train.ravel())

                        # Make predictions
                        X_test = response[-forecast_window:].reshape(-1, 1)
                        predictions = rf_model.predict(X_test)

                        ### CURRENT PROCESS CAPABILITY
                        Cp_norm = round(calculate_cpk(response, LTL, UTL), 4)

                        if Cp_norm < 1:
                            st.error("Watch out! Your current Cpk-value is: {}. Currently, your process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        elif 1 <= Cp_norm <= 1.33:
                            st.warning("Be careful. Your current Cpk-value is: {}. Currently, your process is qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        else:
                            st.success("Awesome! Your current Cpk-value is: {}. Currently, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))


                        best_dist, best_params = best_fit_distribution(response)
                        if best_dist == 'uniform':
                            sample = uniform.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'norm':
                            sample = norm.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'gamma':
                            sample = gamma.rvs(best_params[0], best_params[1], best_params[2], size=1000000)
                        elif best_dist == 'rayleigh':
                            sample = rayleigh.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'weibull_min':
                            sample = weibull_min.rvs(best_params[0], best_params[1], best_params[2], size=1000000)

                        dppm = round(calculate_dppm(response, LTL, UTL), 0)
                        st.write(f'The current amount of defective parts per million for {best_dist} distribution is {dppm}.')


                        # Display Histogram with CDF
                        st.header("Process Distribution Chart")
                        hist_fig = plot_histogram_with_cdf(response, LTL, UTL, process_mean, best_dist)
                        st.plotly_chart(hist_fig)

                        # Interpretation text
                        st.markdown("### How to interpret the Histogram")
                        st.markdown("""
                        - **Density Near Quality Thresholds (LTL and UTL)**: High density near these limits indicates many products are close to being out of specification.
                        - **Density Centered Around Process Mean**: Suggests that most products meet quality standards, and the process is stable.
                        - **Spread of the Density**: Wide spread indicates high variability, while a narrow spread suggests consistency.
                        - **Skewness or Asymmetry**: Skewness could indicate a systematic bias in the production process.
                        - **Multiple Peaks**: May suggest varying quality levels from different sub-processes or machines.
                        - **Continuous Improvement**: Regular analysis of density changes can help in identifying trends for process adjustments.
                        """)


                output_container2 = st.container()

                with output_container2:
                    # Optionally, create a collapsible section
                    with st.expander("Process Chart and Future Process Qualification", expanded=False):

                        
                        #### PREDICTIVE PROCESS CAPABILITY
                        prediction = np.append(response[-(130-forecast_window):], predictions)
                        process_mean_pred = np.mean(prediction)
                        process_std_pred = np.std(prediction)
                        process_min_pred = np.min(prediction)
                        process_max_pred = np.max(prediction)

                        Cp_pred = round(calculate_cpk(prediction, LTL, UTL), 4)

                        if Cp_pred < 1:
                            st.error("Watch out! Your future Cpk-value is: {}. There is a risk, your future process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        elif 1 <= Cp_pred <= 1.33:
                            st.warning("Be careful. Your future Cpk-value is: {}. It might be, your future process qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        else:
                            st.success("Awesome! Your future Cpk-value is: {}. In the future, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))

                        # Detect trend
                        slope, intercept, trend_detected = detect_trend(prediction)

                        # Interpret and display the trend
                        if trend_detected:
                            if slope > 0:
                                trend_description = "Positive (Increasing)"
                            elif slope < 0:
                                trend_description = "Negative (Decreasing)"
                            else:
                                trend_description = "Neutral"
                            
                            st.warning(f"Trend Detected: {trend_description} with slope of {round(slope, 4)}")
                        else:
                            st.warning("No significant Trend detected")
                        

                        ### FORECAST PLOT
                        # st.line_chart(obtained_forecast, "Forecast values")

                        # # #########################################Process Control Chart#############################################
                            # Display Process Control Chart
                        st.header("Process Control Chart")
                        control_chart_fig = plot_process_control_chart(response, predictions, UTL, LTL)
                        st.plotly_chart(control_chart_fig)

    # if st.sidebar.checkbox("MySQL"):

    #     # Create Variables for inserting them in url
    #     MySQL_hostname = st.sidebar.text_input('Hostname')
    #     MySQL_password = st.sidebar.text_input('Password')
    #     MySQL_username = st.sidebar.text_input('Username')
    #     MySQL_dbname = st.sidebar.text_input('DB Name')

    #     myConnection = pymysql.connect(host=MySQL_hostname, user=MySQL_username, passwd=MySQL_password, db=MySQL_dbname)

    if st.sidebar.checkbox("Single CSV-File"):

        upload_file = st.sidebar.file_uploader("Please choose a CSV file:")
                
        if upload_file is not None:

            # convert to pd df
            data = pd.read_csv(upload_file,sep=";", nrows=130) 

            # insert forecast length
            forecast_window = st.slider('Please enter your desired forecast length here:', min_value=1, max_value=20, value=5, step=1) 
            Interest_var = st.selectbox('Please enter the variable you would like to evaluate:', data.columns, 0)

                        # Inside the checkbox block where forecasting is performed
            if st.checkbox("Create Process Qualification Information with the above selected criteria"):

                output_container = st.container()

                with output_container:
                    # Optionally, create a collapsible section
                    with st.expander("Process Distribution and Actual Process Qualification", expanded=False):

                        response = np.array(data[Interest_var])

                        # Ensure the data is a NumPy array of floats
                        response = np.asarray(response, dtype=np.float64)

                        # Remove NaN and infinite values
                        response = response[np.isfinite(response)]

                        # calcuate process stats
                        process_mean = response.mean()
                        process_std = response.std()
                        process_min = response.min()
                        process_max = response.max()
                        process_std = response.std()

                        # Prepare data for Random Forest
                        X_train = response[:-forecast_window].reshape(-1, 1)
                        y_train = response[forecast_window:].reshape(-1, 1)

                        # Train Random Forest model
                        rf_model = train_random_forest(X_train, y_train.ravel())

                        # Make predictions
                        X_test = response[-forecast_window:].reshape(-1, 1)
                        predictions = rf_model.predict(X_test)

                        ### CURRENT PROCESS CAPABILITY
                        Cp_norm = round(calculate_cpk(response, LTL, UTL), 4)

                        if Cp_norm < 1:
                            st.error("Watch out! Your current Cpk-value is: {}. Currently, your process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        elif 1 <= Cp_norm <= 1.33:
                            st.warning("Be careful. Your current Cpk-value is: {}. Currently, your process is qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))
                        else:
                            st.success("Awesome! Your current Cpk-value is: {}. Currently, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/).".format(Cp_norm))


                        best_dist, best_params = best_fit_distribution(response)
                        if best_dist == 'uniform':
                            sample = uniform.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'norm':
                            sample = norm.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'gamma':
                            sample = gamma.rvs(best_params[0], best_params[1], best_params[2], size=1000000)
                        elif best_dist == 'rayleigh':
                            sample = rayleigh.rvs(best_params[0], best_params[1], size=1000000)
                        elif best_dist == 'weibull_min':
                            sample = weibull_min.rvs(best_params[0], best_params[1], best_params[2], size=1000000)

                        dppm = round(calculate_dppm(response, LTL, UTL), 0)
                        st.write(f'The current amount of defective parts per million for {best_dist} distribution is {dppm}.')


                        # Display Histogram with CDF
                        st.header("Process Distribution Chart")
                        hist_fig = plot_histogram_with_cdf(response, LTL, UTL, process_mean, best_dist)
                        st.plotly_chart(hist_fig)

                        # Interpretation text
                        st.markdown("### How to interpret the Histogram")
                        st.markdown("""
                        - **Density Near Quality Thresholds (LTL and UTL)**: High density near these limits indicates many products are close to being out of specification.
                        - **Density Centered Around Process Mean**: Suggests that most products meet quality standards, and the process is stable.
                        - **Spread of the Density**: Wide spread indicates high variability, while a narrow spread suggests consistency.
                        - **Skewness or Asymmetry**: Skewness could indicate a systematic bias in the production process.
                        - **Multiple Peaks**: May suggest varying quality levels from different sub-processes or machines.
                        - **Continuous Improvement**: Regular analysis of density changes can help in identifying trends for process adjustments.
                        """)


                output_container2 = st.container()

                with output_container2:
                    # Optionally, create a collapsible section
                    with st.expander("Process Chart and Future Process Qualification", expanded=False):

                        
                        #### PREDICTIVE PROCESS CAPABILITY
                        prediction = np.append(response[-(130-forecast_window):], predictions)
                        process_mean_pred = np.mean(prediction)
                        process_std_pred = np.std(prediction)
                        process_min_pred = np.min(prediction)
                        process_max_pred = np.max(prediction)

                        Cp_pred = round(calculate_cpk(prediction, LTL, UTL), 4)

                        if Cp_pred < 1:
                            st.error("Watch out! Your future Cpk-value is: {}. There is a risk, your future process is not qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        elif 1 <= Cp_pred <= 1.33:
                            st.warning("Be careful. Your future Cpk-value is: {}. It might be, your future process qualified but not in an ideal state. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))
                        else:
                            st.success("Awesome! Your future Cpk-value is: {}. In the future, your process qualified. Please note: the Cpk-value is highly reliable on a normal distribution. [Learn more about Cpk-values](https://techqualitypedia.com/cp-and-cpk/)".format(Cp_pred))

                        # Detect trend
                        slope, intercept, trend_detected = detect_trend(prediction)

                        # Interpret and display the trend
                        if trend_detected:
                            if slope > 0:
                                trend_description = "Positive (Increasing)"
                            elif slope < 0:
                                trend_description = "Negative (Decreasing)"
                            else:
                                trend_description = "Neutral"
                            
                            st.warning(f"Trend Detected: {trend_description} with slope of {round(slope, 4)}")
                        else:
                            st.warning("No significant Trend detected")
                        

                        ### FORECAST PLOT
                        # st.line_chart(obtained_forecast, "Forecast values")

                        # # #########################################Process Control Chart#############################################
                            # Display Process Control Chart
                        st.header("Process Control Chart")
                        control_chart_fig = plot_process_control_chart(response, predictions, UTL, LTL)
                        st.plotly_chart(control_chart_fig)





