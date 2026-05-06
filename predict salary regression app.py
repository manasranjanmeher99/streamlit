import streamlit as st
import pickle
import numpy as np

model = pickle.load(open(r'C:\Users\ASUS\.spyder-py3\linear_regression_model.pkl','rb'))

st.title("Salary Prediction App")

st.write("this app predict the salary based on years of experience using a simple linear regression model.")

years_experience= st.number_input("Enter years of experience:", min_value=0.0, max_value=50.0, value=1.0, step=0.5)

if st.button("Predict salary"):
    experience_input= np.array([[years_experience]])
    prediction= model.predict(experience_input)

    st.success(f"The prediction salary for {years_experience} years of experience is: ${prediction[0]:,.2f}")

st.write("The model was trained usinhg a dataset of salaries and years of experience.build model by pradict")