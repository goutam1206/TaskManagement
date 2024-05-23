import streamlit as st
import requests
import json


def searchTask():
    st.write("Please Search a Task")
    response = requests.get("http://127.0.0.1:5000/getTask")
    #st.write(response.text)
    if response.status_code == 200:
        response_data = response.content
        #st.write(response.content)
        st.success("Task retrieved Successfully!")
        if len(response_data) > 0:
            st.subheader('Filter Options')
            
            list_of_tasks = []
            c1, c2, c3 = st.columns(3)
            task = c1.selectbox('Search By Status', ["TO_DO", "IN_PROGRESS", "DONE"])
            dateSearch = c2.date_input('Tasks less than')
            desc_Search = c3.text_input('Seach by description')
            if st.button('Search Task'):
                st.write("Searching the data")
    else:
        st.error("Failed to submit task.")
    