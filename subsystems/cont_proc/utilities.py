import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from sklearn.model_selection import train_test_split
import streamlit as st
import pickle

@st.cache_data
def load_dataset(path, skiprows=None, nrows=None):
    dataset = pd.read_csv(path, skiprows=skiprows, nrows=nrows)
    return dataset

@st.cache_data
def stratified_data_split(dataset, target, test_size):
    
    # Define features and labels
    features = dataset.drop(target,axis=1)
    labels = dataset[target]
    
    # Split dataset to train/test
    # The datasets are balanced regarding target = 0 or 1
    x_Train, x_Test, y_Train, y_Test = train_test_split(features,labels,random_state=0,test_size=test_size,stratify=labels)
    
    x_Train[target] = y_Train
    x_Test[target] = y_Test
    
    return x_Train.reset_index(drop=True), x_Test.reset_index(drop=True)

# @st.cache_resource
def create_predtiction_line_graph(data, preds, target_name):
    source = pd.DataFrame({
        'index': data.index,
        target_name+' Negative': data,
        target_name+' Positive': data.where(preds == 1),
        'Positive '+target_name: len(data) * ['Positive '+target_name],
        'Negative '+target_name: len(data) * ['Negative '+target_name],
        })
    
    # x_start, x_end = data.index[0], data.index[0]+100
    x_start, x_end = data.index[0], data.index[-1]
    # y_start, y_end = max(0,data.min()), max(0,data.max())
    y_start, y_end = data.min(), data.max()
    y_start_exp = y_start - (y_end - y_start)*0.15
    y_end_exp = y_end + (y_end - y_start)*0.05

    # x_end
    fig1 = alt.Chart(source).mark_line().encode(
        x=alt.X('index', scale=alt.Scale(domain=[x_start,x_end])).title('Time'),
        y=alt.Y(target_name+' Negative', scale=alt.Scale(domain=[y_start_exp, y_end_exp])).title('Value'),
        color=alt.Color('Negative '+target_name, legend=alt.Legend(title=None, labelFontSize=11, labelOpacity=0.8, direction='vertical',
                                                                    symbolSize=50, orient='bottom-left', offset=0)))
    fig2 = alt.Chart(source).mark_line(point=alt.OverlayMarkDef(size=50)).encode(
        x=alt.X('index', scale=alt.Scale(domain=[x_start,x_end])).title('Time'),
        y=alt.Y(target_name+' Positive', scale=alt.Scale(domain=[y_start_exp, y_end_exp])).title('Value'),
        color=alt.value("#FF0000"),
        shape=alt.Shape('Positive '+target_name, legend=alt.Legend(title=None, labelFontSize=11, labelOpacity=0.8, direction='vertical',
                                                                    symbolSize=50, orient='bottom-left',  offset=0)))

    preds_val, _ = np.unique(preds, return_counts=True)

    if len(preds_val) == 1:
        if preds_val[0] == 0: fig = alt.layer(fig1).properties(height=400).configure_axis(labelAngle=0)
        else: fig = alt.layer(fig2).properties(height=400).configure_axis(labelAngle=0)
    else:
        fig = alt.layer(fig1,fig2).properties(height=400).configure_axis(labelAngle=0)

    return fig

def create_feature_importance_bar_chart(feature_importances):
    fig = px.bar(feature_importances.sort_values(by="Value", ascending=False),
                     x='Value',
                     y='Feature',
                     hover_data=['Value'], 
                     color='Feature',
                     orientation='h')
    fig.update_layout(showlegend=False)

    return fig

@st.cache_resource
def get_csv_rows(csv_path):

    row_count = 0
    with open(csv_path, 'r') as csvfile:
        for _ in enumerate(csvfile):
            row_count += 1
            
    return row_count

def save_model_features_names(feature_list, model_name):
    with open('features//'+model_name+'_feature_names.pkl', 'wb') as file:
        pickle.dump(feature_list, file)

def load_model_features_names(model_name):
    with open('features//'+model_name+'_feature_names.pkl', 'rb') as file:
        feature_list = pickle.load(file)
    return feature_list

def highlight_rows(row):
    if row[-1] == 1:
        return ['background-color: rgba(255, 0, 64, 0.3)'] * len(row)
    else:
        return [''] * len(row)
    
def generate_warning(preds, target):
    count = np.count_nonzero(preds == 1)
    precentage = count/len(preds)*100
    if precentage == 0:
        # warning_txt = target+" has not been positive anywhere in the samples."
        warning_txt = ""
    else:
        warning_txt = target+' is estimated to be present in: {:.2f}% of samples'.format(precentage)
    return warning_txt

# def close_consumer(consumer):
#     if consumer!= None:
#         consumer.close()
#         print("Consumer CLOSED Util")

def data_converter(df):
    df.drop(columns=['fechahora'], inplace=True)
    df.dropna(inplace=True)
    
    return df
