import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.preprocessing import LabelEncoder,OneHotEncoder

model = pickle.load(open('reg.pkl','rb'))


def run():
    
    st.sidebar.info('This app is created to forecast fraud values in web channels')

    st.title("Fraud Volume Forecast App")
    
    Year = st.number_input('Year', min_value=1, max_value=3000, value=2014)
    Channel = st.selectbox('Channel', ['ATM', 'Internet Banking', 'Mobile', 'POS', 'Web', 'eCommerce' ])
    Value = st.number_input('Value', min_value=10, max_value=999999999999, value=20659546)

    output=""

    input_dict = {'Year' : Year, 'Channel' : Channel, 'Value' : Value}
    input_df = pd.DataFrame([input_dict])
    le = LabelEncoder()
    input_df['Channel'] = le.fit_transform(input_df['Channel'])


    if st.button("Forecast"):
        inputs=np.array(input_df)
        prediction = model.predict(inputs)
        prediction = np.round(prediction)
        output = '#' + str(prediction)

        st.success('The forcasted fraud volume is {}'.format(output))
        # read data
        data = pd.read_csv('fraud_sheet.csv')
        data['Value'] = data['Value'].str.replace(',', '').astype(float)
        data['Volume'] = data['Volume'].str.replace(',', '').astype(float)
        data = data[data['Year'] == Year]
        fig1, ax1 = plt.subplots()
        ax1.pie(data['Value'], labels=data['Channel'], autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  
        st.pyplot()

        st.subheader('Recommendations and Implementation')
        st.table(pd.DataFrame({
            'Object':['Customer', 'Customer/Organisation', 'Customer', 'Organisation', 'Organisation', 'Organisation'],

            'Susceptible Channel': ['Point of Sale(POS)',
                            'Ecommerce Internet banking Web payment',
                        'Ecommerce Internet banking POS Web payment', 
                        'POS', 
                        'ATM',
                        'Ecommerce Internet banking POS Web payment'],
            
            'Threat': ['Interference with transmitted data which may lead to theft of identity and or card details', 
                    'Malware on customers device affect payment verification leading to sham transactions such as charge back and double charge scam',
                    'Poor cyber hygiene from the Organisations end can result in data been exposed and breach of privacy ', 
                    'POS receiving several irrelevant  requests leading to a potential denial of service', 
                    'Physical security(ATM break-in) Insert Skimmers(Placed in card slots to capture card information)',
                    'fraud control evasion, Fraudulent transfer of funds'],
           
            'Proposed Action': ['Decision makers should use platforms with secure protocols and encryption.', 
                    'Decision makers should implement several levels of authentication for  every customer', 
                    'Decision makers should implement good cyber hygiene such as ensuring all applications are updated when required. Implement multi factor authentication and ensure good cyber security policies',
                    'Decision makers should implement POS encryption Ensure the most recent version of the application and operating system is running Ensure regular audit of security system',
                    'Decision makers should there are security personnel, cctv etc to physically protect ATMs Routine checks should be made by experts of each organization to avoid skimmers',
                    'Decision makers should ensure robust cryptography protocol, encryption and several levels of authentication']
            
        }))
        st.subheader('Projection')
        st.write('1. If decision makers do not address fears related to online payment, customers will be discouraged from making online transaction with these businesses. This may reduce revenue and eventually lead to business shut down.')

        st.write('2. “Protecting websites against hackers will minimize customers’ fears of e-payment which can increases revenue and business growth.” If decision makers allow their business site to be vulnerable to hackers it discourages customers from making transaction on their sites which may reduce revenue and eventually lead to business shut down.')

st.subheader('Revenue Projection')
Current_Revenue = st.number_input('Current Revenue', min_value=1, max_value=999999999999)
Previous_Revenue = st.number_input('Previous Revenue', min_value=10, max_value=999999999999)


if st.button("revenue increase"):
    increase= ((Current_Revenue - Previous_Revenue)/Previous_Revenue) * 100
    st.success('The projected revenue is {}'.format(increase))


if __name__ == '__main__':
    run()
