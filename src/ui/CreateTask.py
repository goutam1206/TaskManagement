import streamlit as st
from datetime import date
import requests
import json

def createTask():
    st.write("Please Create a Task")
    task_name = st.text_input("Ener the task name")
    task_description = st.text_area("Task Description","", height = 200, key="desc")
    due_date = st.date_input("Task completion Date", date.today())
    if st.button('Submit Task'):
        # Check if the input is empty
        if not task_name:
            st.error("Task Name is required. Please enter a value.")
            st.stop()
        # Check if the input is empty
        if not task_description:
            st.error("Task Description is required. Please enter a value.")
            st.stop()
        # Check if the input is empty
        if not due_date:
            st.error("Task completion date is required. Please enter a value.")
            st.stop()
        if due_date < date.today():
            st.error("The due date cannot be in the past.")
            st.stop()
        else:
            st.write("Task Details Submitted:")
            st.write(f"Task Name: {task_name}")
            st.write(f"Task Details: {task_description}")
            st.write(f"Due Date: {due_date}")
            data = {
                "task_name"     : task_name,
                "task_details"  : task_description,
                "due_date"      : str(due_date),
                "status"        : "TO_DO"
            }

            # Send data to the Flask server
            response = requests.post("http://127.0.0.1:5000/addTask", json=data)
            
            if response.status_code == 200:
                response_data = response.json()
                st.success("Task Submitted Successfully!")
                st.json(response_data)
            else:
                st.error("Failed to submit task.")

