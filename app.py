import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.preprocessing import LabelEncoder

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
        output = '$' + str(prediction)
        # read data
        data = pd.read_csv('fraud_data_sheet.csv')
        data['Value'] = data['Value'].str.replace(',', '').astype(float)
        data['Volume'] = data['Volume'].str.replace(',', '').astype(float)
        data = data[data['Year'] == Year]
        fig1, ax1 = plt.subplots()
        ax1.pie(data['Value'], labels=data['Channel'], autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  
        st.pyplot()

        st.success('The forcasted fraud volume is {}'.format(output))

        st.subheader('Recommendations and Implementation')
        st.table(pd.DataFrame({
            'Target':['User', 'User','User','User','User', 'Service Provider', 'Service Provider', 'Service Provider', 'Service Provider'],

            'Vulnerability': ['Over the Air (OTA) transmission between phone and Point of Sale(POS) (NFC reader)',
                            'Inadvertent installation of malicious software on a mobile phone by the user',
                        'Absence of two- factor authentication ', 'Changing or replacing the mobile phone', 'Smartphone internet and geolocation capabilities','POS system accepts OTA transmissions',
                        'POS devices are installed at merchant premises', 'Lack of Digital Rights Management (DRM) on the mobile device', 'Weakness of Global System for mobile communication(GSM) encryption for OTA transmission; SMS data in clear text on mobile network'],
            
            'Threat': ['Interception of Traffic', 'Downloaded applications intercept of authentication data',
                    'User masquerading', 'Configuration and setup complecity', 'Malware on the mobile device; poor data protection controls at merchant/payment processor', 'Malicious party floods POS system with meaningless requests',
                    'Masquerade attacks; tampering with POS', 'Mobile device user illegally distributes content; e.g ringtone, video, games, etc', 'Message modification, a replay of transactions, evasion of fraud controls'],
            
            'Risk': ['Identity theft, Information disclosure, replay attacks', 'fraudulent transactions, procider liabilities', 'fraudulent transactions, procider liabilities',
                    'Reduced adoption of the technology, "security by obscurity"','Data disclosure and privacy infringement; profiling of user behaviour','Denial of Service (DoS)',
                    'Theft of service, replay, message modification', 'Theft of content, Digital piracy, a risk to the provider for digital rights infringement, loss of revenue to the content provider of merchant',
                    'Theft of Service or content, loss of revenue, illegal transfer of funds'],
            
            'Proposed Action': ['Trusted Platform Module(TPM), secure protocols, encryption', 'Authentication of both user (PIN) and application ( digital signature by trusted third-party), TPM', 'Two-Factor authentication',
                    'A simplified user interface, security parameters in TPM set by a trusted party', 'User control of geolocation features, cryptographically supported privacy, trusted platform module,vetted authorization and accounting',
                    'Request filtering at reader based on mobile device0- reader relative geometry', 'POS vendor vetting, message authenticators, vetted authorization and accounting', 'Trusted Platform Module (TPM) design, cryptographically supported DRM',
                    'Strong Cryptographic protocols, SMS message authenticators, encryption']
            
        }))
        st.subheader('Projection')
        st.write('1. If decision makers do not address fears related to online payment, customers will be discouraged from making online transaction with these businesses. This may reduce revenue and eventually lead to business shut down.')

        st.write('2. “Protecting websites against hackers will minimize customers’ fears of e-payment which can increases revenue and business growth.”')
        st.markdown('If decision makers allow their business site to be vulnerable to hackers it discourages customers from making transaction on their sites which may reduce revenue and eventually lead to business shut down.')

if __name__ == '__main__':
    run()
