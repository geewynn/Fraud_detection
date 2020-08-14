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

    #from PIL import Image
    #image = Image.open('logo.png')
    #image_hospital = Image.open('hospital.jpg')

    #st.image(image,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.info('This app is created to predict patient hospital charges')
    st.sidebar.success('https://www.pycaret.org')
    
    #st.sidebar.image(image_hospital)

    st.title("Fraud Volume Prediction App")

    if add_selectbox == 'Online':

        Year = st.number_input('Year', min_value=1, max_value=3000, value=2013)
        Channel = st.selectbox('Channel', ['ATM', 'Internet Banking', 'Mobile', 'POS', 'Web', 'eCommerce' ])
        Value = st.number_input('Value', min_value=10, max_value=999999999999, value=25600750)

        output=""

        input_dict = {'Year' : Year, 'Channel' : Channel, 'Value' : Value}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = '$' + str(output)

        st.success('The output is {}'.format(output))

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()
