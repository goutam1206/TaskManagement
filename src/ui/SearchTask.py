import streamlit as st
import requests
from datetime import datetime
import json


def searchTask():
    st.write("Please Search a Task")
    response = requests.get("http://127.0.0.1:5000/getTask")
    
    if response.status_code == 200:
        response_data = response.json()  # Convert response to JSON
        st.success("Tasks retrieved Successfully!")

        if response_data:
            st.subheader('Filter Options')

            # Search by status
            options = ['Status', 'Date', 'Description']
            search_option = st.selectbox("Choose an option:", options, key="search_option")


            wanted_tasks = response_data  # Default to all tasks

            if search_option == "Status":
                status_options = ["TO_DO", "IN_PROGRESS", "DONE"]
                task_status = st.selectbox('Search By Status', status_options, key="status_option")
                if task_status:
                    wanted_tasks = filter_tasks_by_status(response_data, task_status)
            elif search_option == "Date":
                dateSearch = st.date_input('Task completion less than', key="date_option")
                if dateSearch:
                    wanted_tasks = filter_tasks_by_date(response_data, dateSearch)
            elif search_option == 'Description':
                desc_Search = st.text_area("Search by description", key="desc_option")
                if desc_Search:
                    wanted_tasks = filter_tasks_by_description(response_data, desc_Search)

            if st.button('Search Task'):
                st.write("Searching the data")
                for task in wanted_tasks:
                    st.markdown(create_tile(task), unsafe_allow_html=True)

                if not wanted_tasks:
                    st.info("No tasks match the search criteria.")
        else:
            st.error("No tasks found.")
    else:
        st.error("Failed to retrieve tasks.")



def filter_tasks_by_description(tasks, description):
    return [task for task in tasks if description.lower() in task.get('task_details', '').lower()]


def filter_tasks_by_status(task_list, status):
    """
    This function filters tasks based on the selected status.
    
    :param task_list: List of task dictionaries
    :param status: Status to filter tasks by
    :return: List of tasks with the specified status
    """
    if status == "Select":
        return task_list
    else:
        return [task for task in task_list if task.get('status') == status]

def filter_tasks_by_date(task_list, date):
    """
    This function filters tasks based on the selected status.
    
    :param task_list: List of task dictionaries
    :param status: Status to filter tasks by
    :return: List of tasks with the specified status
    """
    if date == "" or date is None:
        return task_list
        # Convert date string to datetime object
    selected_date = datetime.combine(date, datetime.min.time()).date()
    return [task for task in task_list if datetime.strptime(task.get('due_date'), '%Y-%m-%d').date() < selected_date]


# Function to create a tile for each task
def create_tile(task):
    tile_template = f"""
    <div style='
        background-color: #f0f0f5; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1); 
        margin: 10px 0;'>
        <h3 style='color: #2c3e50;'>{task['task_name']}</h3>
        <p style='color: #2c3e50;'><strong>Details:</strong> {task['task_details']}</p>
        <p style='color: #2c3e50;'><strong>Due Date:</strong> {task['due_date']}</p>
        <p style='color: #2c3e50;'><strong>Status:</strong> {task['status']}</p>

    </div>
    """
    return tile_template
