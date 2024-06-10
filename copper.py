

import streamlit as st
import numpy as np
from datetime import date
import pickle

#page configuration
st.set_page_config(page_title='Industrial Copper Modeling')

st.markdown(f'<h2 style="text-align: center;">Industrial Copper Modeling</h2>',
                unsafe_allow_html=True)

#button style and text style functions
def style_submit_button():

  st.markdown("""
                  <style>
                  div.stButton > button:first-child {
                                                      background-color: #367F89;
                                                      color: white;
                                                      width: 70%}
                  </style>
              """, unsafe_allow_html=True)


def style_prediction():

  st.markdown(
          """
          <style>
          .center-text {
              text-align: center;
              color: orange
          }
          </style>
          """,
          unsafe_allow_html=True
      )

#user input options
class options:

    country_values = [25.0, 26.0, 27.0, 28.0, 30.0, 32.0, 38.0, 39.0, 40.0, 77.0, 78.0,
                       79.0, 80.0, 84.0, 89.0, 107.0, 113.0]

    status_values = ['Won', 'Lost', 'Draft', 'To be approved', 'Not lost for AM',
                    'Wonderful', 'Revised', 'Offered', 'Offerable']

    status_dict = {'Lost':0, 'Won':1, 'Draft':2, 'To be approved':3, 'Not lost for AM':4,
                'Wonderful':5, 'Revised':6, 'Offered':7, 'Offerable':8}

    item_type_values = ['W', 'WI', 'S', 'PL', 'IPL', 'SLAWR', 'Others']

    item_type_dict = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_values = [2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0,26.0,
                          27.0, 28.0, 29.0, 38.0, 39.0, 40.0, 41.0, 42.0, 56.0, 58.0, 59.0,
                          65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 87.5]

    product_ref_values = [611728, 611733, 611993, 628112, 628117, 628377, 640400, 640405,640665,164141591,
                          164336407, 164337175, 929423819, 1282007633, 1332077137, 1665572032, 1665572374,
                          1665584320, 1665584642, 1665584662, 1668701376, 1668701698, 1668701718, 1668701725,
                          1670798778, 1671863738, 1671876026, 1690738206, 1690738219, 1693867550,
                          1693867563, 1721130331, 1722207579]

#function for regression and classification
class prediction:

    def regression():

        with st.form('Regression'):

            col1,col2,col3 = st.columns([0.5,0.1,0.5])

            with col1:

                item_date = st.date_input(label='Item Date', min_value=date(2020,2,7),
                                        max_value=date(2021,4,1), value=date(2020,2,7))

                quantity_log = st.text_input(label='Quantity Tons (Min: 0.00001 & Max: 1000000000)')

                country = st.selectbox(label='Country', options=options.country_values)

                item_type = st.selectbox(label='Item Type', options=options.item_type_values)

                thickness_log = st.text_input(label='Thickness (Min: 0.18 & Max: 2500)')
                
                product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)


            with col3:

                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1),
                                            max_value=date(2022,1,1), value=date(2020,8,1))

                customer = st.text_input(label='Customer ID (Min: 12458 & Max: 2147483647)')

                status = st.selectbox(label='Status', options=options.status_values)

                application = st.selectbox(label='Application', options=options.application_values)

                width = st.text_input(label='Width (Min: 1.0 & Max: 2990)')

                st.write('')
                st.write('')
                button = st.form_submit_button(label='SUBMIT')
                style_submit_button()
             
        if button:
            with open(r'/content/drive/MyDrive/Copper_project/Regression_model.pkl', 'rb') as f:
                model = pickle.load(f)

            user_data = np.array([[np.log(float(customer)),
                                country,
                                options.status_dict[status],
                                options.item_type_dict[item_type],
                                application,
                                width,
                                product_ref,
                                np.log(float(quantity_log)),
                                np.log(float(thickness_log)),
                                item_date.day, item_date.month, item_date.year,
                                delivery_date.day, delivery_date.month, delivery_date.year]])

            y_pred = model.predict(user_data)          
            selling_price = np.exp(y_pred[0])           
            selling_price = round(selling_price, 2)
            return selling_price
    
    def classification():

        with st.form('Classification'):

            col1,col2,col3 = st.columns([0.5,0.1,0.5])

            with col1:

                item_date = st.date_input(label='Item Date', min_value=date(2020,2,7), 
                                        max_value=date(2021,4,1), value=date(2020,2,7))
                
                quantity_log = st.text_input(label='Quantity Tons (Min: 0.00001 & Max: 1000000000)')

                country = st.selectbox(label='Country', options=options.country_values)

                item_type = st.selectbox(label='Item Type', options=options.item_type_values)

                thickness_log = st.text_input(label='Thickness (Min: 0.18 & Max: 2500)')

                product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)


            with col3:

                delivery_date = st.date_input(label='Delivery Date', min_value=date(2020,8,1), 
                                            max_value=date(2022,1,1), value=date(2020,8,1))
                
                customer = st.text_input(label='Customer ID (Min: 12458 & Max: 2147483647)')

                selling_price_log = st.text_input(label='Selling Price (Min: 0.1 & Max: 100001015)')

                application = st.selectbox(label='Application', options=options.application_values)

                width = st.text_input(label='Width (Min: 1.0 & Max: 2990)')

                st.write('')
                st.write('')
                button = st.form_submit_button(label='SUBMIT')
                style_submit_button()

        if button:
            
            with open(r'/content/drive/MyDrive/Copper_project/classification_model.pkl', 'rb') as f:
                model = pickle.load(f)
            user_data = np.array([[np.log(float(customer)), 
                                country, 
                                options.item_type_dict[item_type], 
                                application, 
                                width, 
                                product_ref, 
                                np.log(float(quantity_log)), 
                                np.log(float(thickness_log)),
                                np.log(float(selling_price_log)),
                                item_date.day, item_date.month, item_date.year,
                                delivery_date.day, delivery_date.month, delivery_date.year]])
          
            y_pred = model.predict(user_data)
            status = y_pred[0]
            return status

#main streamlit page 
tab1, tab2 = st.tabs(['PREDICT SELLING PRICE', 'PREDICT STATUS'])

with tab1:

    try:
        selling_price = prediction.regression()
        if selling_price:
            style_prediction()
            st.markdown(f'### <div class="center-text">Predicted Selling Price = {selling_price}</div>', unsafe_allow_html=True)
            
    except ValueError:
        col1,col2,col3 = st.columns([0.26,0.55,0.26])
        with col2:
            st.warning('##### Quantity Tons / Customer ID is empty')

with tab2:

    try:
        status = prediction.classification()
        if status == 1:
            style_prediction()
            st.markdown(f'### <div class="center-text">Predicted Status = Won</div>', unsafe_allow_html=True)

        elif status == 0:
            style_prediction()
            st.markdown(f'### <div class="center-text">Predicted Status = Lost</div>', unsafe_allow_html=True)          
    
    except ValueError:

        col1,col2,col3 = st.columns([0.15,0.70,0.15])

        with col2:
            st.warning('##### Quantity Tons / Customer ID is empty')






