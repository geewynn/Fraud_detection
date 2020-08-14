from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np

model = load_model('deployment_1')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

#     add_selectbox = st.sidebar.selectbox(
#     "How would you like to predict?",
#     ("Online"))

    st.sidebar.info('This app is created to predict patient hospital charges')
   

    st.title("Fraud Volume Prediction App")

    #if add_selectbox == 'Online':add_selectbox = st.sidebar.selectbox(
    # "How would you like to predict?",
    # ("Online",))

    Year = st.number_input('Year', min_value=1, max_value=3000, value=2013)
    Channel = st.selectbox('Channel', ['ATM', 'Internet Banking', 'Mobile', 'POS', 'Web', 'eCommerce' ])
    Value = st.number_input('Value', min_value=10, max_value=999999999999, value=25600750)

    output=""

    input_dict = {'Year' : Year, 'Channel' : Channel, 'Value' : Value}
    input_df = pd.DataFrame([input_dict])

    if st.button("Predict"):
        output = predict(model=model, input_df=input_df)
        output = '$' + str(output)

    st.success('The predicted fraud value is {}'.format(output))


if __name__ == '__main__':
    run()
